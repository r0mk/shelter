resource "oci_core_instance" "proxy" {
  availability_domain =  data.oci_identity_availability_domain.ad.name
  compartment_id      = var.tenancy_ocid
  display_name        = "r0mkproxy"
  shape               = "VM.Standard.E2.1.Micro"

  create_vnic_details {
    subnet_id        = oci_core_subnet.oci_subnet.id
    display_name     = "primaryvnic"
    assign_public_ip = true
    hostname_label   = "r0mkproxy"
  }

  source_details {
    source_type = "image"
   source_id   = data.oci_core_image.ubuntu_2004_min.id
 }

  metadata = {
    ssh_authorized_keys = var.public_key
  }
}

output "instance_private_ips" {
  value = [oci_core_instance.proxy.*.private_ip]
}
output "instance_public_ips" {
  value = [oci_core_instance.proxy.*.public_ip]
}

