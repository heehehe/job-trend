## Getting Stared
Terraform을 사용한 GCP VM 생성

### Prerequisites
- gcp service account json 파일
- install terraform
    - https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli

### Setup
- gcp service account json파일을 git repository home의 private_dir 경로에 생성한다.
    ```
    job_trend/private_dir/gcp_service_account.json
    ```
- terraform 및 ansible에서 사용할 gcp account name과 gcp에 인증할 ssh key file name을 export 해준다

    ```
    export TF_VAR_vm_user="{gcp account name}"
    export TF_VAR_vm_ssh_key="{ssh key file name}"
    export TF_VAR_home=$HOME (.ssh/ 가 있는 홈 경로)
    ```
- terraform.tfvars 작성  
    - terraform.tfvars.template 예시에 맞춰 작성 후 file 이름을 "terraform.tfvars" 로 변경

### Run
- vm이 생성되면서 ansible/hosts 파일 생성됨
    ```
    terraform init
    terraform validate  # main.tf 파일의 코드 에러 검증
    ./create_vm.sh
    ```
### Remove
- terraform으로 생성한 vm은 terraform으로 삭제
    ```
    terraform destroy
    'yes' 입력
    ```
