variable region {
    default = {
        asia = "asia-northeast3"
    }
} 
variable zone {
    default = {
        asia = "asia-northeast3-c"
    }

}
variable machine {
    default = {
        micro = "f1-micro"
        e2_medium = "e2-medium"

    }
    
}
variable image {
    default = {
        ubuntu_2004 = "ubuntu-os-cloud/ubuntu-2004-lts"
    }
}
variable "project_id" { }
variable "credentials_file" { }
variable "account_name" {}
variable "root_passwd" {  }
variable "docker_compose_url" {}
variable "docker_install_sh" {}
variable "ssh_pub_key" {
  
}
