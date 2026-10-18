import asyncio
from copy import deepcopy

from agents import Agent, RunContextWrapper
import pytest

from bid_agent_sidecar import sdk_tools
from bid_agent_sidecar.rewrite_candidate_completeness import apply_recall_group_review
from bid_agent_sidecar.rewrite_discovery_handoff import expand_shared_problem_contracts
from bid_agent_sidecar.rewrite_review_revision import expand_frozen_revision
from test_body_recovery_tool_contract import context, invoke
from test_rewrite_discovery_handoff import _shared_contract
from test_body_recovery_tool_contract import _prepare_rewrite_problem_test_context
from test_sdk_tools import _record_rewrite_problem_transaction, _rewrite_problem_item, _rewrite_evidence_content_risk_plan


def prepared():
    ctx = context()
    records, decisions, proofs = {}, {}, {}
    handles = [f"rewrite-candidate:{i}" for i in range(48)]
    for i, h in enumerate(handles):
        proof = {"detail": "full", "bodyLatestVersion": "v1", "bodyContentHash": f"hash{i}"}
        proofs[h] = proof
        records[h] = {"candidateHandle": h, "bodyLatestVersion": "v1", "bodyContentHash": f"hash{i}",
                      "lastRead": proof}
        decisions[h] = {"decision": "repair", "businessReason": f"原判断{i}", "problemFamily": "删除指定业务",
                        "nodeEdit": {"expectedChange": f"旧改法{i}", "preserveFacts": [f"原事实{i}"]},
                        "fullBodyRead": proof}
    ctx.rewrite_problem_candidates = {"records": records}
    ctx.rewrite_dependency_state = {"factRecallReview": {
        "mode": "grouped_review", "mainReviewRequired": True, "complete": True,
        "candidateCount": 48, "currentGroupIndex": 2,
        "groups": [{"groupId": f"g{i}", "candidateHandles": handles[i*24:(i+1)*24],
                    "candidates": [], "fullBodyReadEvidence": {"records": {h: proofs[h] for h in handles[i*24:(i+1)*24]}}} for i in range(2)],
        "dispositions": {h: "repair" for h in handles}, "dispositionRecords": decisions,
    }}
    return ctx, handles


def correction(handle, **extra):
    return {"candidateHandle": handle, "decision": "repair", "businessReason": "本节全部属于删除目标，无其他独立义务",
            "problemFamily": "删除指定业务", "nodeEdit": {"expectedChange": "删除本节全部目标文字", "preserveFacts": []}, **extra}


def test_two_revisions_replace_old_edits_keep_other_46_and_replay_idempotent():
    ctx, hs = prepared()
    before = deepcopy(ctx.rewrite_dependency_state["factRecallReview"])
    changes = [correction(hs[0]), correction(hs[30])]
    result = apply_recall_group_review(ctx, group_id="g1", decisions=changes)
    assert result["ok"] and result["revisedCandidateCount"] == 2
    now = ctx.rewrite_dependency_state["factRecallReview"]
    for h in hs:
        if h not in {hs[0], hs[30]}:
            assert now["dispositionRecords"][h] == before["dispositionRecords"][h]
    expanded, gap = expand_shared_problem_contracts(ctx, {"sharedProblem": _shared_contract()})
    assert gap is None and len(expanded["problems"]) == 48
    for p in expanded["problems"]:
        assert p["expectedChange"] == ("删除本节全部目标文字" if p["candidateHandle"] in {hs[0], hs[30]} else before["dispositionRecords"][p["candidateHandle"]]["nodeEdit"]["expectedChange"])
    assert apply_recall_group_review(ctx, group_id="g1", decisions=changes)["alreadyComplete"]


@pytest.mark.parametrize("changes", [
    lambda hs: [correction(hs[0]), correction(hs[0])],
    lambda hs: [correction("unknown")],
    lambda hs: [correction(hs[0]), correction(hs[1], nodeEdit={"expectedChange": "", "preserveFacts": []})],
])
def test_invalid_revision_does_not_partially_replace_decisions(changes):
    ctx, hs = prepared()
    before = deepcopy(ctx.rewrite_dependency_state)
    result = apply_recall_group_review(ctx, group_id="g0", decisions=changes(hs))
    assert not result["ok"] and ctx.rewrite_dependency_state == before


def test_changed_disposition_does_not_keep_old_write_target():
    ctx, hs = prepared()
    result = apply_recall_group_review(ctx, group_id="g0", decisions=[
        {"candidateHandle": hs[0], "decision": "preserve", "businessReason": "复核原文已经满足用户要求"}])
    assert result["ok"]
    expanded, gap = expand_shared_problem_contracts(ctx, {"sharedProblem": _shared_contract()})
    assert gap is None and len(expanded["problems"]) == 47
    assert hs[0] not in {p["candidateHandle"] for p in expanded["problems"]}


def test_mixed_final_contract_overrides_then_uses_current_frozen_edits_after_review_retired():
    ctx, hs = prepared()
    patch = {**_shared_contract(candidateHandle=hs[0]), "expectedChange": "删除全部目标文字", "preserveFacts": []}
    expanded, gap = expand_shared_problem_contracts(ctx, {"sharedProblem": _shared_contract(), "problems": [patch]})
    assert gap is None and len(expanded["problems"]) == 48
    ctx.rewrite_problem_transaction = {"status": "frozen", "problems": expanded["problems"]}
    ctx.rewrite_dependency_state = {"status": "cleared"}
    second = {**_shared_contract(candidateHandle=hs[1]), "expectedChange": "另一个目标的修订"}
    again, gap = expand_frozen_revision(ctx, {"sharedProblem": _shared_contract(), "problems": [second]})
    assert gap is None and again["problems"][0]["expectedChange"] == "删除全部目标文字"
    assert len(again["problems"]) == 48 and again["problems"][1]["expectedChange"] == "另一个目标的修订"


def test_partial_frozen_problem_list_cannot_silently_cancel_other_targets():
    ctx, hs = prepared()
    full, gap = expand_shared_problem_contracts(ctx, {"sharedProblem": _shared_contract()})
    assert gap is None
    ctx.rewrite_problem_transaction = {"status": "frozen", "problems": full["problems"]}
    before = deepcopy(ctx.rewrite_problem_transaction)
    patch = {**_shared_contract(candidateHandle=hs[0]), "expectedChange": "修订"}
    _, gap = expand_frozen_revision(ctx, {"problems": [patch]})
    assert gap["reasonCode"] == "rewrite_problem_revision_targets_missing"
    assert ctx.rewrite_problem_transaction == before
    for selector in ({"sharedProblem": _shared_contract(candidateHandles=[hs[0]])},
                     {"sharedProblems": [_shared_contract(candidateHandles=[hs[0]])]}):
        # The discovery state is retired by freeze in the actual tool path.
        retired = deepcopy(ctx)
        retired.rewrite_dependency_state = {"status": "cleared"}
        _, gap = expand_frozen_revision(retired, selector)
        assert gap["reasonCode"] == "rewrite_problem_revision_targets_missing"
        assert retired.rewrite_problem_transaction == before
    _, gap = expand_frozen_revision(ctx, {"problems": [patch, {**patch, "candidateHandle": "new-target"}]})
    assert gap["reasonCode"] == "rewrite_problem_revision_targets_missing"
    assert ctx.rewrite_problem_transaction == before
    _, gap = expand_frozen_revision(ctx, {"problems": [patch], "coverageReview": [
        {"candidateHandles": hs[1:], "decision": "exclude", "businessReason": "复核后确认已满足本次目标"}]})
    assert gap is None


@pytest.mark.asyncio
async def test_tool_available_after_review_and_execution_rejected_without_state_change(monkeypatch):
    monkeypatch.setenv("BID_AGENT_ROUTE_PROFILE", "ac_bounded_direct_body")
    ctx, hs = prepared()
    agent = Agent(name="test", tools=sdk_tools.create_bid_tools())
    assert "review_recall_candidate_group" in {t.name for t in await agent.get_all_tools(RunContextWrapper(ctx))}
    ctx.content_generation_started = True
    before = deepcopy(ctx.rewrite_dependency_state)
    result = await invoke(sdk_tools.review_recall_candidate_group, ctx, group_id="g0", decisions=[correction(hs[0])])
    assert result["reasonCode"] == "recall_revision_execution_started"
    assert ctx.rewrite_dependency_state == before


@pytest.mark.asyncio
async def test_frozen_revision_redirects_to_final_contract_without_changing_state(monkeypatch):
    monkeypatch.setenv("BID_AGENT_ROUTE_PROFILE", "ac_bounded_direct_body")
    ctx, hs = prepared()
    ctx.rewrite_problem_transaction = {"status": "frozen", "candidateHandles": hs}
    before = deepcopy(ctx.rewrite_dependency_state)
    result = await invoke(sdk_tools.review_recall_candidate_group, ctx, group_id="g0", decisions=[correction(hs[0])])
    assert result["reasonCode"] == "recall_revision_use_problem_set"
    assert ctx.rewrite_dependency_state == before


@pytest.mark.asyncio
async def test_actual_final_contract_revision_keeps_second_target_and_invalidates_bound_plan(monkeypatch):
    monkeypatch.setenv("BID_AGENT_ROUTE_PROFILE", "ac_bounded_direct_body")
    ctx, _, leaf, other = _prepare_rewrite_problem_test_context(monkeypatch)
    old_first = _rewrite_problem_item(leaf)
    old_first["expectedChange"] = "第一处按旧决定保留专属办理流程"
    result = await asyncio.to_thread(_record_rewrite_problem_transaction, ctx,
                                    old_first, _rewrite_problem_item(other))
    assert result["ok"]
    plan = _rewrite_evidence_content_risk_plan(plan_id="before", intent_id="before", action_type="section_rewrite",
                                              target_location="已确认问题章节", evidence_origin_refs=[])
    assert (await invoke(sdk_tools.record_task_action_plan, ctx, plan=plan, active_intent_id="before"))["ok"]
    original = deepcopy(ctx.rewrite_problem_transaction)
    first, second = original["problems"]
    rejected = await invoke(sdk_tools.record_rewrite_problem_set, ctx, problem_set={
        "sharedProblem": _shared_contract(candidateHandles=[first["candidateHandle"]])})
    assert rejected["reasonCode"] == "rewrite_problem_revision_targets_missing"
    assert ctx.rewrite_problem_transaction == original and ctx.active_task_action_plan
    patch = {**_shared_contract(candidateHandle=first["candidateHandle"]), "expectedChange": "删除指定目标文字，保持其余内容",
             "preserveFacts": ["原有人员和面积"]}
    revised = await invoke(sdk_tools.record_rewrite_problem_set, ctx,
                           problem_set={"sharedProblem": _shared_contract(), "problems": [patch]})
    assert revised["ok"] and revised["superseded"] and revised["newPlanRequired"]
    assert not ctx.active_task_action_plan and not ctx.changed_node_ids
    assert {p["currentLeafId"] for p in ctx.rewrite_problem_transaction["problems"]} == {leaf, other}
    by_handle = {p["candidateHandle"]:p for p in ctx.rewrite_problem_transaction["problems"]}
    assert by_handle[first["candidateHandle"]]["expectedChange"] == patch["expectedChange"]
    assert by_handle[second["candidateHandle"]]["expectedChange"] == second["expectedChange"]
    instruction = sdk_tools._active_problem_generation_instruction(ctx, "执行本次完整任务")
    assert patch["expectedChange"] in instruction
    assert second["expectedChange"] in instruction
    assert first["expectedChange"] not in instruction
