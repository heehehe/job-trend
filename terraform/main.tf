
# data "template_file" "ssh_key" {
#   template = file("${path.module}/../private_dir/${var.ssh_pub_key}")
# }
provider "google" {
  credentials = "${file("${path.module}/../private_dir/${var.credentials_file}")}"
  project = var.project_id
  region = var.region.asia
}

resource "google_compute_address" "static_ip" {
  name = "vm-static-ip"
  project = var.project_id
  region  = var.region.asia
}

resource "google_compute_instance" "default" {
  name = "terraform-gce"
  machine_type = var.machine.e2_medium
  zone = var.zone.asia

  boot_disk {
    initialize_params {
        image = var.image.ubuntu_2004
        
    }
  }

  network_interface {
    network = "default"
    access_config {
      # nat_ip = google_compute_address.static_ip.address

    }
  }

  metadata = {
    ssh-keys = "${var.vm_user}:${file("${var.home}/.ssh/${var.vm_ssh_key}.pub")}"
    
  }

  metadata_startup_script = <<-EOF
              #!/bin/bash
              sudo apt-get update
              sudo apt-get install python3-pip -y
              pip3 install apache-airflow
              EOF

}

# resource "null_resource" "output_to_file" {
#   provisioner "local-exec" {
#     # command = "echo ${google_compute_instance.default.network_interface.0.access_config.0.nat_ip} > ${path.module}/../private_dir/ip.txt"
#     command = "VM_IP=${google_compute_instance.default.network_interface.0.access_config.0.nat_ip}"
    
#   }
# }


output "public_ip" {
  value = "${google_compute_instance.default.network_interface.0.access_config.0.nat_ip}"
}
