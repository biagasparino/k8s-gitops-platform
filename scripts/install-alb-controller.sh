#!/usr/bin/env bash
# Installs the AWS Load Balancer Controller on the EKS cluster (it turns Ingress objects into ALBs).
# Prereqs: eksctl, kubectl, helm, aws cli authenticated, cluster created from infra/eksctl/cluster.yaml
set -euo pipefail

CLUSTER="${CLUSTER:-tasks-eks}"
REGION="${REGION:-us-east-1}"
ACCOUNT_ID="$(aws sts get-caller-identity --query Account --output text)"
POLICY_NAME="AWSLoadBalancerControllerIAMPolicy"
POLICY_VERSION="v2.8.2"

curl -fsSL -o /tmp/alb-iam-policy.json \
  "https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/${POLICY_VERSION}/docs/install/iam_policy.json"

aws iam create-policy --policy-name "$POLICY_NAME" \
  --policy-document file:///tmp/alb-iam-policy.json 2>/dev/null || echo "Policy already exists, reusing it."

eksctl create iamserviceaccount \
  --cluster "$CLUSTER" --region "$REGION" \
  --namespace kube-system --name aws-load-balancer-controller \
  --attach-policy-arn "arn:aws:iam::${ACCOUNT_ID}:policy/${POLICY_NAME}" \
  --approve --override-existing-serviceaccounts

helm repo add eks https://aws.github.io/eks-charts
helm repo update
helm upgrade --install aws-load-balancer-controller eks/aws-load-balancer-controller \
  --namespace kube-system \
  --set clusterName="$CLUSTER" \
  --set serviceAccount.create=false \
  --set serviceAccount.name=aws-load-balancer-controller

kubectl -n kube-system rollout status deploy/aws-load-balancer-controller --timeout=180s
