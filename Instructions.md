# This file lists the steps involved in creating the CI/CD pipeline.

## Dockerfile
First create a docker file for the app. Make sure if the front-end is using Streamlit, then the `8501` port number should be exposed. Also make sure that you're using `docker run -d -p 8501:8501` command in the `main.yaml` file.

## AWS IAM Config
Create an IAM user in AWS with the following policies:
* `AmazonEC2ContainerRegistryFullAccess`
* `AmazonEC2FullAccess`

Make sure to save the **access key** and **secret access key**.

## AWS ECR
Create a repo in AWS ECR and save the URI.

## AWS EC2
Create an EC2 instance with required specifications. In the security group, add port number `8501` if using Streamlit, else add port number `8080`. Connect to the instance and run the following commands.

* `sudo apt-get update -y`
* `sudo apt-get upgrade`
* `curl -fsSL https://get.docker.com -o get-docker.sh`
* `sudo sh get-docker.sh`
* `sudo usermod -aG docker ubuntu`
* `newgrp docker`

## Self-Hosted Runner
GitHub Actions allows you to run your CI/CD workflows on virtual machines, and these virtual machines are referred to as "runners." A self-hosted runner is a type of GitHub runner that you set up and manage yourself. It runs your GitHub Actions workflows in your own environment, such as an EC2 instance.

Go to `setting>actions>runner>new self hosted runner> choose os` and then run the commands one by one in EC2 machine. 

## Setup GitHub Secrets
Go to `Settings > Secrets & Variables > Actions` and add the following secrets

* `AWS_ACCESS_KEY_ID`
* `AWS_SECRET_ACCESS_KEY`
* `AWS_REGION`
* `AWS_ECR_LOGIN_URI`
* `ECR_REPOSITORY_NAME`

The pipeline is now complete!
