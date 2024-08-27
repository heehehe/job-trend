variable region {
    default = {
        asia = "asia-northeast3"
    }
} 
variable zone {
    default = {
        asia = "asia-northeast3-b"
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
variable "project_id" {}
variable "credentials_file" {}
# variable "ssh_pub_key" {}
variable "vm_user" {}
variable "vm_name" {}
variable "vm_ssh_key" {}
variable "home" {}