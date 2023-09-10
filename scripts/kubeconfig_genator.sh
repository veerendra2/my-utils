#!/bin/bash
# Author: Veerendra K
# Description: Generates kubeconfig file for service account

SERVICE_ACCOUNT=$1
USER="user"
if [ -z $1 ]
then
 echo "[.] Please specify Service Account name"
 echo "Usage: ./kubeconfig_generator.sh <service_account> <namespace>"
 exit 1
fi
if [ -z $2 ]
then
 echo "[.] Please specify namespace"
 echo "Usage: ./kubeconfig_generator.sh <service_account> <namespace>"
 exit 1
fi
echo "[+]  Make sure you have kubectl binary and kubeconfig in ~/.kube/ directory"
sleep 1
echo "[+] Changing kubeconfig context to '$2'"
kubectl config set-context `kubectl config current-context` --namespace=$2
secret=`kubectl get sa $SERVICE_ACCOUNT -o jsonpath='{.secrets[0].name}'`
if [[ $secret = *"token"* ]]; then
  echo "[*] Found secret $secret"
else
  secret=`kubectl get sa $SERVICE_ACCOUNT -o jsonpath='{.secrets[1].name}'`
  echo "[*] Found secret $secret"
fi
if [ -z $secret ];
then
 echo "[-] Not able to retrieve the specified service account name!"
 exit 1
fi
echo "[*] Fetching service account's CA"
kubectl get secret $secret -o "jsonpath={.data['ca\.crt']}" > ca.crt
echo "[*] Fetching $SERVICE_ACCOUNT token"
user_token=`kubectl get secret $secret -o "jsonpath={.data['token']}" | base64 -d`
context=`kubectl config current-context`
context_name=`kubectl config get-contexts $context | awk '{print $3}' | tail -n 1`
endpoint=`kubectl config view -o jsonpath="{.clusters[?(@.name == \"$context_name\")].cluster.server}"`
echo "[*] Creating a backup of exiting kubeconfig"
mv ~/.kube/config .
echo "[*] Generating kubeconfig with service account -> $SERVICE_ACCOUNT"
kubectl config set-cluster cluster-openshift --embed-certs=true --server=$endpoint --certificate-authority=./ca.crt
kubectl config set-credentials $USER --token=$user_token
kubectl config set-context $2 --cluster=cluster-openshift --user=$USER --namespace=$2
kubectl config use-context $2
mv ~/.kube/config $SERVICE_ACCOUNT.kubeconfig
mv config ~/.kube/config
mv $SERVICE_ACCOUNT.kubeconfig config
rm -f ca.crt
#kubectl adm policy add-scc-to-user anyuid system:serviceaccount:$2:$2
