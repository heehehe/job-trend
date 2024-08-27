## Getting Started

### Prerequisites
- .ssh directory for VM (~/.ssh/) & vm 접근 시 사용할 ssh key
- VM 
- VM public ip address (terraform 실행 시 hosts file에 존재)
- docker

### Setup
- docker로 ansible container 생성
    ```
    ./docker-build.sh
    docker exec -it ansible-container /bin/bash
    ```

### Run
- container 내부에서 ansible playbook 실행
    ```
    # cd /home/ansible-setup/
    # ansible-playbook playbook.yml
    ```
    - 현재 vm에 docker, docker compose까지만 설치됨