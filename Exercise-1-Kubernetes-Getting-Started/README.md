\# Exercise 1 - Kubernetes Getting Started



\## Objective



Deploy an Nginx application as a Kubernetes Pod using Minikube and expose it using a NodePort Service.



\## Prerequisites



\- Docker Desktop

\- Minikube

\- kubectl



\## Environment



\- OS: Windows 11

\- Minikube: v1.39.0

\- Kubernetes: v1.37.0

\- kubectl: v1.37.1

\- Minikube driver: Docker



\## Steps



\### 1. Start Minikube



```powershell

minikube start --driver=docker --cpus=2 --memory=2048

