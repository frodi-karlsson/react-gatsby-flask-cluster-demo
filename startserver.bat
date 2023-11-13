minikube start
minikube addons enable ingress
minikube addons enable metrics-server
minikube addons enable dashboard
minikube addons enable registry
minikube addons enable registry-creds

kubectl apply -f ./app.yaml;
