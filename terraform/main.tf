
data "template_file" "ssh_key" {
  template = file("${path.module}/../private_dir/${var.ssh_pub_key}")
}
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
      nat_ip = google_compute_address.static_ip.address

    }
  }

  metadata = {
    ssh-keys="${var.account_name}:${data.template_file.ssh_key.rendered}"
  }

  metadata_startup_script = <<-EOF
              #!/bin/bash
              sudo apt-get update
              sudo apt-get install python3-pip -y
              pip3 install apache-airflow
              EOF

}


# ${file("${path.root}/install/${var.docker_install_sh}")}
#               cd /home/${var.account_name}
#               mkdir airflow-docker
#               cd airflow-docker
#               mkdir -p ./dags ./logs ./plugins ./config
#               echo -e "AIRFLOW_UID=$(id -u)" > .env