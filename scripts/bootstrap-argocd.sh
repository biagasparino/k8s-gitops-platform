#!/usr/bin/env bash
# Installs ArgoCD and hands the cluster over to GitOps by applying the single root Application.
set -euo pipefail
cd "$(dirname "$0")/.."

kubectl create namespace argocd --dry-run=client -o yaml | kubectl apply -f -
kubectl apply -n argocd --server-side -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl -n argocd rollout status deploy/argocd-server --timeout=300s

# Credentials Secrets must exist BEFORE the first sync (they are never stored in Git).
for ns in tasks-dev tasks-staging tasks-prod; do
  ./scripts/create-db-secret.sh "$ns"
done

kubectl apply -f gitops/bootstrap/root-app.yaml

echo
echo "ArgoCD UI:   kubectl -n argocd port-forward svc/argocd-server 8081:443   ->  https://localhost:8081"
echo "Admin login: admin / $(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d)"
echo "(change that password and delete the initial secret after first login)"
