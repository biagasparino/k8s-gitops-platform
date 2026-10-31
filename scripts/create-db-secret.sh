#!/usr/bin/env bash
# Creates the database credentials Secret with a RANDOM password, outside of Git.
# Usage: ./scripts/create-db-secret.sh <namespace>     e.g. tasks-dev
# (In real production use External Secrets Operator or Sealed Secrets instead.)
set -euo pipefail

NAMESPACE="${1:?Usage: create-db-secret.sh <namespace>}"
PASSWORD="$(head -c 24 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 24)"

kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -

kubectl -n "$NAMESPACE" create secret generic tasks-db-credentials \
  --from-literal=username=tasks_user \
  --from-literal=password="$PASSWORD" \
  --dry-run=client -o yaml | kubectl apply -f -

echo "Secret tasks-db-credentials ready in namespace $NAMESPACE (password not printed)."
