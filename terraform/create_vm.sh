#!/bin/bash

# Apply Terraform configuration
terraform apply -auto-approve

# Store Terraform output in environment variable
echo -e "[webservers]\nweb1 ansible_host=$(terraform output public_ip)" > $PWD/../ansible/hosts

# Print the value of the environment variable
echo "vm ip is $VM_IP"

