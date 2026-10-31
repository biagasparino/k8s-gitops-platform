# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.0.0] - 2026-10-30
### Added
- Sample application: React (Vite) frontend, FastAPI backend, PostgreSQL, with unit tests and Dockerfiles.
- Helm chart `tasks-platform`: Namespace, Deployment, Service, Ingress, ConfigMap, Secret, ServiceAccount,
  RBAC (read-only Role + RoleBinding), resource requests/limits, startup/liveness/readiness probes,
  HorizontalPodAutoscaler, PodDisruptionBudget, StatefulSet for PostgreSQL, NetworkPolicies.
- ArgoCD "app of apps": AppProject plus dev/staging (auto-sync) and prod (manual sync) Applications.
- Per-environment values files under `gitops/environments/`.
- `eksctl` cluster definition (IRSA, EBS CSI, metrics-server, NetworkPolicy enforcement) and bootstrap scripts.
- GitHub Actions: CI (ruff, pytest, vitest, helm lint, kubeconform, docker build), release
  (build + push to GHCR + update GitOps tag) and promotion-by-pull-request.
- Local kind setup (`scripts/kind-up.sh`).
- English and Portuguese documentation with diagrams.
