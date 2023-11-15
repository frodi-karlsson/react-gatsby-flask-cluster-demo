# What is this?
This is a demonstration of a multi-container application running on kubernetes. It's a simple web app that allows you to simulate actions on historical stock data through a front-end, which then sends requests to a back-end that applies the actions to the data and stores the results.

The stack is:
- Front-end: React, Gatsby
- Back-end: Python, Flask, Pandas, yfinance

My kubernetes setup is:
- Minikube
- Docker Desktop
- kubectl

There is no persistence layer, so the data is lost when the back-end container is restarted.
This is on purpose to keep the demo simple.

# Setup
Assuming you are running my kubernetes setup, you can run the following commands to get the app running:

`minikube start`

`& minikube -p minikube docker-env --shell powershell | Invoke-Expression` for ps
`eval $(minikube docker-env)` for linux

`docker-compose build`

`minikube addons enable ingress`

`kubectl apply -f kubernetes/webapp.yaml`

`minikube tunnel`

Otherwise I'll have to assume you're proficient enough with kubernetes to get it running yourself.

# Accessing the app

I don't have a linux machine to test this on, but on windows you can access the app at `kubernetes.docker.internal`. On linux I don't think that entry is added to the hosts file, so you'll have to add it yourself at `/etc/hosts`. You can also add a custom entry and replace all mentions of the host with that.

These are: 2 in the kubernetes/webapp.yaml file, and 1 in the website/src/components/stocks/StockHandler.ts file.

# Front-end
The front-end is a simple react app that allows you to buy stocks and progress the simulation time.
It's built with react and gatsby. Here is an image of the admittedly very ugly front-end:
![Front-end](https://gcdnb.pbrd.co/images/i6GwTiNPBGUt.png?o=1)

# Back-end
The back-end runs on the yfinance library, which is a python library that allows you to get historical stock data from yahoo finance. The server itself is an api running on flask that allows you to buy stocks and progress the simulation time. Not all of the functionality is exposed through the front-end, as I didn't want to spend too much time on this.

# Kubernetes
We have a deployment with a service each for the frontend and backend, with an ingress to route traffic to the frontend service. The ingress is configured to route traffic to the frontend service on the `/api` path to the backend service.

There are no resource or security constraints to keep this simple, but in a real environment you would want to set those in the yaml.
