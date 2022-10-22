# NLP-Deployment-Kubernetes

We will deploy NLP multilabel model using Kubernetes which is a technology that allows us to automatically deploy, scale and operate containers.

## Prerequisites

Kind (Kubernetes in Docker): is a tool that will allow us to create a local Kubernetes cluster in our computer for learning and developing.

kubectl: the Kubernetes command-line tool, used to run commands against Kubernetes clusters.

## Usage 

Setting up a local Kubernetes cluster with Kind
```bash
kind create cluster
```

Before we run the deployment, we need to load our image into our cluster nodes.
```bash
kind load docker-image nlp_multilabel:v5
```

We can now apply our deployment.yaml file to our cluster:
```bash
kubectl apply -f deployment.yml 
```

With the service.yaml file created, we can now deploy it:
```bash
kubectl apply -f service.yml 
```

kubectl get pod
kubectl get deployment

You can now check the state of the service with kubectl get service and test it with the curl command.
```bash
kubectl get service
```



## Port Forwarding

IMPORTANT: when checking the service status, you will most likely find that the LoadBalancer service we created has <pending> as its external IP value. We did not configure our cluster to assign IP's to LoadBalancers, so you will have to make use of port forwarding for testing.

```bash
kubectl port-forward service/nlp-service 8080:80
```

## Testing the API
```bash
curl -v http://127.0.0.1:8080/predict?url=https://www.alwatanvoice.com/arabic/news/2022/10/08/1492784.html
```

## Next step

As next step, we will deploy our application to AWS EKS