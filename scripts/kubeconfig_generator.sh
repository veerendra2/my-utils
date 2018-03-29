#!/bin/bash
# Author: Veerendra Kakumanu
# Description: Creates kubeconfig for specified service account
# Usage: ./kubeconfig_generator.sh <service_account_name>
# Dependencies: kubectl, jq, config in ~/.kube/

SERVICE_ACCOUNT=$1
echo "[+]  Make sure you have kubectl binary, jq binary and kubeconfig in ~/.kube/ directory"
echo ""
sleep 1
secret=`kubectl get sa $SERVICE_ACCOUNT -o jsonpath='{.secrets[1].name}'`
if [ -z $secret ];
then
 echo "[-] Not able to retrive the specified service account name!"
 exit 1
fi
echo "[*] Fetching service account's CA"
kubectl get secret $secret -o json | jq -r '.data["ca.crt"]' | base64 -d > ca.crt
echo "[*] Fetching $SERVICE_ACCOUNT token"
user_token=`kubectl get secret $secret -o json | jq -r '.data["token"]' | base64 -d`
context=`kubectl config current-context`
context_name=`kubectl config get-contexts $context | awk '{print $3}' | tail -n 1`
endpoint=`kubectl config view -o jsonpath="{.clusters[?(@.name == \"$context_name\")].cluster.server}"`
echo "[*] Creating a backup of exiting kubeconfig"
mv ~/.kube/config .
echo "[*] Generating kubeconfig with service account -> $SERVICE_ACCOUNT"
kubectl config set-cluster cluster-openshift --embed-certs=true --server=$endpoint --certificate-authority=./ca.crt
kubectl config set-credentials spinnaker --token=$user_token
kubectl config set-context spinnaker --cluster=cluster-openshift --user=spinnaker --namespace=spinnaker
kubectl config use-context spinnaker
mv ~/.kube/config $SERVICE_ACCOUNT.kubeconfig
mv config ~/.kube/config
echo "[*] Generated kubeconfig file: `pwd`/$SERVICE_ACCOUNT.kubeconfig"
