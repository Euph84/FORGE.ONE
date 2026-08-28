# LLM Deployment Fit & Cost Analyzer — V0.3

Conservative first-pass Apify Actor for vLLM deployment sizing.

## Included
- PASS / RISK / FAIL
- weight-memory estimate
- explicit KV-cache risk proxy
- benchmark-required gate
- conservative starting vLLM arguments
- optional user-supplied GPU economics
- one PPE event: `analysis-completed`

## Deliberate limits
No live provider prices are invented. Exact KV-cache sizing waits for model architecture metadata.
The Actor writes the result before triggering the paid event.

## V0.3 billing hardening
See `APIFY_PUBLISH_CHECKLIST.md`. One visible analysis maps to one custom `analysis-completed` charge; default dataset-item billing must be removed in Console. Memory is capped at 256 MB.
