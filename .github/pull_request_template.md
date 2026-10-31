## What changed

## How it was verified
- [ ] `pytest` / `vitest` pass
- [ ] `helm lint` and `helm template | kubeconform` pass (CI runs these)
- [ ] No secrets, passwords or tokens in the diff

## Rollout notes
<!-- dev auto-syncs; staging auto-syncs after promotion; prod needs a manual Sync in ArgoCD -->
