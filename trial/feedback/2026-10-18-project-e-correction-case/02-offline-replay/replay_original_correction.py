"""Replay the real rejected corrections; no network or model calls."""
import ast
from copy import deepcopy
import json
from pathlib import Path
import sys
from types import SimpleNamespace

B=Path(__file__).resolve().parent
baseline=len(sys.argv)>1
R=Path(sys.argv[1]) if baseline else B.parents[1]
sys.path.insert(0,str(R))
if baseline:sys.path.insert(1,str(B.parents[1]))
from bid_agent_sidecar.rewrite_candidate_completeness import apply_recall_group_review
from bid_agent_sidecar.rewrite_discovery_handoff import expand_shared_problem_contracts

root=B.parent/'editpro-priority-fixes-20261018/evidence/D'
decisions={};groups=[];correction=None;final=None
for line in (root/'state/sdk-traces.private.jsonl').read_text(encoding='utf-8').splitlines():
    x=json.loads(line);d=x.get('payload',{}).get('span_data',{})
    if x['event']!='span_end' or d.get('type')!='function':continue
    args=json.loads(d['input'])
    if d['name']=='review_recall_candidate_group':
        hs=[]
        for v in args['decisions']:decisions[v['candidateHandle']]=v;hs.append(v['candidateHandle'])
        groups.append({'groupId':args['group_id'],'candidateHandles':hs,'candidates':[]})
    if d['name']=='_editpro_rejected_call':correction=json.loads(args['requested_arguments'])
    if d['name']=='record_rewrite_problem_set' and args['problem_set'].get('problems'):final=args['problem_set']
transaction=json.loads(next((root/'state/continuations').glob('*.json')).read_text(encoding='utf-8'))['rewriteProblemTransaction']
registry={};proofs={}
for p in transaction['problems']:
    h=p['candidateHandle'];proof={k:p[k] for k in ('bodyLatestVersion','bodyContentHash')};proof['detail']='full';proofs[h]=proof
    registry[h]={'candidateHandle':h,**proof,'lastRead':proof}
for g in groups:g['fullBodyReadEvidence']={'records':{h:proofs[h] for h in g['candidateHandles'] if h in proofs}}
review={'mode':'grouped_review','complete':True,'mainReviewRequired':True,'candidateCount':len(decisions),
    'groups':groups,'currentGroupIndex':len(groups),'dispositions':{h:d['decision'] for h,d in decisions.items()},
    'dispositionRecords':{h:{'decision':d['decision'],'problemFamily':d.get('problemFamily',''),'businessReason':d['businessReason'],
        **({'nodeEdit':{'expectedChange':d['expectedChange'],'preserveFacts':d['preserveFacts']},'fullBodyRead':proofs[h]} if d['decision']=='repair' else {})}
        for h,d in decisions.items()}}
ctx=SimpleNamespace(rewrite_dependency_state={'factRecallReview':review},rewrite_problem_candidates={'records':registry},structured_rewrite_context={})
original=deepcopy(review)
ds=[]
for d in correction['decisions']:
    ds.append({**d,'nodeEdit':{'expectedChange':d['expectedChange'],'preserveFacts':d['preserveFacts']}})
revised=apply_recall_group_review(ctx,group_id=correction['group_id'],decisions=ds)
expanded,gap=expand_shared_problem_contracts(ctx,final)
if baseline:
    result={'correctionAcknowledged':revised.get('ok'),'alreadyComplete':revised.get('alreadyComplete'),
            'actualDecisionChanged':ctx.rewrite_dependency_state['factRecallReview']!=original,
            'finalCorrectionRejected':gap is not None,'reasonCode':(gap or {}).get('reasonCode'),
            'scope':'same original correction calls against immutable current-version baseline; no network or save'}
    assert not result['actualDecisionChanged'] and result['finalCorrectionRejected']
    (B/'ORIGINAL-CORRECTION-BASELINE.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))
    sys.exit(0)
assert revised['ok'] and revised['revisionAccepted']
assert gap is None and len(expanded['problems'])==48
patches={p['candidateHandle']:p for p in final['problems']}
for p in expanded['problems']:
    if p['candidateHandle'] in patches:assert p['expectedChange']==patches[p['candidateHandle']]['expectedChange']
    else:assert p['expectedChange']==original['dispositionRecords'][p['candidateHandle']]['nodeEdit']['expectedChange']
result={'realPreviouslyRejectedGroupCorrectionAccepted':True,'realPreviouslyRejectedTwoFinalCorrectionsAccepted':True,
        'repairTargetsRetained':48,'correctedTargets':2,'other46ExpectedChangesUnchanged':True,
        'oldRetargetingNotInCorrectedContracts':all('公积金' not in p['expectedChange'] for p in expanded['problems'] if p['candidateHandle'] in patches),
        'scope':'offline original decision replay and contract expansion; no save or model inference'}
(B/'ORIGINAL-CORRECTION-REPLAY.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
