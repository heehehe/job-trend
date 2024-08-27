#!/bin/bash

# Apply Terraform configuration
terraform apply -auto-approve

terraform_output=$(terraform output public_ip)
# Store Terraform output in environment variable
echo -e "[webservers]\nweb1 ansible_host=$terraform_output" > $PWD/../ansible/hosts

# Print the value of the environment variable
echo "vm ip is $terraform_output"
