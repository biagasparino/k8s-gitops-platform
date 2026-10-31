#!/usr/bin/env bash
# Runs the whole platform on a local kind cluster, with Helm (no AWS, no ArgoCD).
set -euo pipefail
cd "$(dirname "$0")/.."

kind create cluster --config kind/kind-config.yaml || true
kubectl config use-context kind-tasks-local

echo ">> ingress-nginx"
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
kubectl -n ingress-nginx rollout status deploy/ingress-nginx-controller --timeout=180s

echo ">> build and load images into the cluster"
docker build -t tasks-backend:local app/backend
docker build -t tasks-frontend:local app/frontend
kind load docker-image tasks-backend:local tasks-frontend:local --name tasks-local

echo ">> secret + helm install"
./scripts/create-db-secret.sh tasks-local
helm upgrade --install tasks helm/tasks-platform \
  --namespace tasks-local -f kind/values-kind.yaml --wait --timeout 5m

echo
echo "Open http://localhost:8080"
