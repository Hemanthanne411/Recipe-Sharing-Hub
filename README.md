
# Recipe Sharing Microservices Application

## 📝 Project Description

This is a modern, microservices-based web application for sharing recipes. The application allows users to sign up, log in, add their own recipes, and search for recipes shared by others. It is designed and deployed using **Kubernetes** to demonstrate best practices in cloud-native development.

## ✨ Key Features

  * **User Authentication**: Secure user registration and login functionality.
  * **Recipe Management**: Users can create, list, and view their personal recipes.
  * **Recipe Search**: A robust search functionality to find recipes by title or ingredients.
  * **Persistent Data Storage**: All user and recipe data is stored in a persistent database.
  * **Containerized Services**: The entire application is containerized using Docker.
  * **Microservices Architecture**: The application logic is separated into independent, single-purpose services.

## 🏛️ Architecture

The application is built on a microservices architecture, with each component running as a separate service. All services are orchestrated by **Kubernetes** to ensure scalability and reliability.

### Services

  * **`user-service`**: A Flask-based API Gateway and frontend server. It handles user authentication (signup, login) and acts as a proxy, forwarding requests to the `recipe-service`.
  * **`recipe-service`**: A Flask-based API that manages all recipe data. It communicates directly with the database.
  * **`postgres`**: A PostgreSQL database for persistent data storage.

## 🚀 Getting Started

To run this project on your local machine using Minikube, follow these simple steps.
 The Docker images are pre-built and hosted publicly, so there is no need to build them, make sure Docker Desktop is running in the background.

### Prerequisites

  * [**Minikube**](https://minikube.sigs.k8s.io/docs/start/)
  * [**kubectl**](https://kubernetes.io/docs/tasks/tools/install-kubectl/)

### 1\. Start Minikube

Start your Minikube cluster.

```sh
minikube start
```

### 2\. Create Kubernetes Secret

This command creates a Kubernetes Secret to securely store the database password, which is a required step before deployment.

```sh
kubectl create secret generic postgres-password-secret --from-literal=password=mysecretpassword6432
```

### 3\. Deploy to Kubernetes

Apply all the Kubernetes manifest files to deploy your application, database, and configurations. Change the directory to / k8s

```sh
kubectl apply -f .
```

### 4\. Check Pod Status

Verify that all your microservice pods are running correctly.

```sh
kubectl get pods
```

### 5\. Access the Application

The `user-service` is exposed as a `NodePort` service. To get the URL to access the application, run this command and open the URL in your web browser.

```sh
minikube service user-service --url
```

## 📦 Project Structure

```
.
├── user-service/
│   ├── app.py
│   ├── templates/
│   │   ├── ...(html templates)
│   └── Dockerfile
├── recipe-service/
│   ├── app.py
│   └── Dockerfile
├── k8s/
│   ├── postgres-init-configmap.yaml
│   ├── postgres-pv-claim.yaml
│   ├── postgres-service.yaml
│   ├── postgres-deployment.yaml
│   ├── userservice-service.yaml
│   ├── user-deployment.yaml
│   ├── recipeservice-service.yaml
│   └── recipe-deployment.yaml
└── README.md
```

## 📄 License

This project is licensed under the MIT License.