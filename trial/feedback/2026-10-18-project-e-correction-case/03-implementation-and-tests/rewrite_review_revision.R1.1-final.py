"""Revise Main-owned decisions through the existing validation and state owner."""
from copy import copy, deepcopy
from typing import Any, Mapping


def revise_completed_review(context: Any, decisions: list[Mapping[str, Any]]) -> dict[str, Any]:
    from .rewrite_candidate_completeness import apply_recall_group_review, project_recall_review_manifest_for_agent

    original = context.rewrite_dependency_state["factRecallReview"]
    records = original.get("dispositionRecords") or {}
    handles = [str(d.get("candidateHandle") or "") for d in decisions]
    if (not handles or len(set(handles)) != len(handles)
            or any(h not in records for h in handles)
            or any(not str(d.get("businessReason") or "").strip() for d in decisions)):
        return {"ok": False, "reasonCode": "recall_revision_invalid",
                "message": "仅提交已审候选的完整新判断和具体业务理由；不得重复句柄或新增未审目标。"}

    # Validate on a temporary review; invalid/partial input cannot discard the
    # existing decisions or change the authoritative cursor.
    selected = set(handles)
    candidates, proofs = [], {}
    for group in original.get("groups") or []:
        candidates.extend(deepcopy(c) for c in group.get("candidates") or []
                          if c.get("candidateHandle") in selected)
        proofs.update({h: deepcopy(p) for h, p in
                       ((group.get("fullBodyReadEvidence") or {}).get("records") or {}).items()
                       if h in selected})
    scratch = copy(context)
    scratch.rewrite_dependency_state = deepcopy(context.rewrite_dependency_state)
    scratch.rewrite_dependency_state.pop("factRecallCoverage", None)
    scratch.rewrite_problem_candidates = deepcopy(context.rewrite_problem_candidates)
    scratch.rewrite_dependency_state["factRecallReview"] = {
        **deepcopy(original), "complete": False, "status": "reviewing", "currentGroupIndex": 0,
        "candidateCount": len(handles), "dispositions": {}, "dispositionRecords": {}, "autoAcceptedCandidates": [],
        "groups": [{"groupId": "revision", "candidateHandles": handles, "candidates": candidates,
                    "fullBodyReadEvidence": {"status": "ready", "detail": "full", "records": proofs}}],
    }
    result = apply_recall_group_review(scratch, group_id="revision", decisions=decisions)
    accepted = scratch.rewrite_dependency_state["factRecallReview"]
    if not result.get("ok") or not accepted.get("complete"):
        return {**result, "ok": False, "revisionAccepted": False,
                "message": "修订未接纳，原判断与其他目标保持；补齐本次修订缺项后重提。"}
    semantic_keys = ("decision", "businessReason", "problemFamily", "uncertaintyScope", "nodeEdit")
    changed = [h for h in handles if any(records[h].get(k) != accepted["dispositionRecords"][h].get(k)
                                         for k in semantic_keys)]
    if changed:
        updated = deepcopy(original)
        for handle in changed:
            updated["dispositions"][handle] = accepted["dispositions"][handle]
            updated["dispositionRecords"][handle] = accepted["dispositionRecords"][handle]
        updated.pop("noChangeConclusion", None)
        context.rewrite_dependency_state["factRecallReview"] = updated
    projection = project_recall_review_manifest_for_agent(
        context.rewrite_dependency_state["factRecallReview"], observations_only=True)
    return {"ok": True, "status": "complete", "complete": True, "revisionAccepted": bool(changed),
            "alreadyComplete": not changed, "revisedCandidateCount": len(changed),
            "reviewedCandidateCount": len(records), "unreviewedCount": 0, "nextGroup": "",
            "review": projection, "nextRecommendedAction": projection["nextRecommendedAction"]}


def expand_frozen_revision(context: Any, payload: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any] | None]:
    """The frozen transaction owns current edits after discovery is retired.

    This only assembles inputs; the existing handler still checks execution,
    scope, identities, current bodies and invalidates the previous plan.
    """
    result = deepcopy(dict(payload))
    transaction = getattr(context, "rewrite_problem_transaction", {}) or {}
    common = result.get("sharedProblem")
    patches = result.get("problems") or []
    if transaction.get("status") != "frozen":
        return result, None
    if (not isinstance(common, Mapping) or not patches or result.get("sharedProblems")
            or any(common.get(k) for k in ("candidateHandles", "candidateResultSetRef", "reviewProblemFamily"))):
        # Check the resolved set for every supported selection form. Changing
        # from explicit problems to a shared selector cannot drop old goals.
        from .rewrite_discovery_handoff import expand_shared_problem_contracts
        expanded, gap = expand_shared_problem_contracts(context, result)
        if not gap and any(result.get(k) for k in ("problems", "sharedProblem", "sharedProblems")):
            known = {p.get("candidateHandle") for p in transaction.get("problems") or []}
            selected = {p.get("candidateHandle") for p in expanded.get("problems") or [] if isinstance(p, Mapping)}
            excluded = {h for review in result.get("coverageReview") or [] if isinstance(review, Mapping)
                        and review.get("decision") in {"exclude", "defer"} and str(review.get("businessReason") or "").strip()
                        for h in review.get("candidateHandles") or []}
            if not (known-selected).issubset(excluded):
                return result, {"ok": False, "recoverable": True, "reasonCode": "rewrite_problem_revision_targets_missing",
                                "message": "本次仅列出部分旧目标，不能将其余待办默认为取消。原执行合同保持。",
                                "nextRecommendedAction": "用problems列出本次完整修订，并补一个省略范围选择字段的sharedProblem；程序保留其他目标。确需排除旧目标时，在coverageReview逐项填写exclude/defer及业务理由。"}
        return result, None
    originals = transaction.get("problems") or []
    known = {p.get("candidateHandle") for p in originals}
    overrides = {}
    for patch in patches:
        handle = patch.get("candidateHandle") if isinstance(patch, Mapping) else None
        if not handle or handle not in known or handle in overrides:
            return result, {"ok": False, "recoverable": True, "reasonCode": "rewrite_problem_revision_target_invalid",
                            "message": "局部修订仅使用本次已冻结目标的真实句柄，不增加目标或重复句柄。"}
        overrides[handle] = patch
    internal = {"identity", "currentLeafId", "bodyLatestVersion", "bodyContentHash", "baselineRiskClaims", "bodyReviewObservation"}
    result["problems"] = [{**{k: deepcopy(v) for k, v in original.items() if k not in internal},
                           **deepcopy(overrides.get(original.get("candidateHandle"), {}))} for original in originals]
    result.pop("sharedProblem", None)
    if "sharedRequirements" not in result and transaction.get("sharedRequirements"):
        result["sharedRequirements"] = deepcopy(transaction["sharedRequirements"])
    return result, None
