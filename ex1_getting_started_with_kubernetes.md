# Kubernetes Hands-On Exercise Series

## Exercise 1: Getting Started with Kubernetes

This exercise helps us understand the basic working of Kubernetes by running a simple Nginx web application inside a Kubernetes cluster.

## Business Problem – Zepto Example

Imagine you are a **DevOps Engineer at Zepto**. The product team has created a simple web application that displays the storefront and delivery status for customers.

Your task is to deploy this application using Kubernetes so that it can run properly, can be managed easily, and can be scaled later.

For this exercise, we use the **Nginx container image** to represent the Zepto web application.

## Goal

The goal of this exercise is to create our first Kubernetes Pod, run the Nginx application inside it, and access the application through a browser.

## Prerequisites

The following tools are required:

- Docker Desktop
- Minikube
- kubectl

Docker Desktop should be installed and running because Minikube uses Docker to create the local Kubernetes cluster.

## Steps: Deploy Nginx as a Kubernetes Pod

### 1. Start the Kubernetes Cluster

Start Minikube using the Docker driver:

```bash
minikube start --driver=docker

This command starts a local Kubernetes cluster using Docker.

### 2. Check if the Cluster is Ready

After starting Minikube, check whether the Kubernetes node is ready:

```bash
kubectl get nodes