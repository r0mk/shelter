resource "oci_core_instance" "hq" {
  availability_domain =  data.oci_identity_availability_domain.ad.name
  compartment_id      = var.tenancy_ocid
  display_name        = "hq"
  shape               = "VM.Standard.E2.1.Micro"

  create_vnic_details {
    subnet_id        = oci_core_subnet.oci_subnet.id
    display_name     = "primaryvnic"
    assign_public_ip = true
    hostname_label   = "hq"
  }

  source_details {
    source_type = "image"
    #source_id   = data.oci_core_image.ubuntu_2004_min.id
    source_id   = "ocid1.image.oc1.eu-frankfurt-1.aaaaaaaala3albkmkwmgkpbe5nkbfwmhjw74e4yzzrzrvwe7tgalsblataua"

 }

  metadata = {
    ssh_authorized_keys = var.public_key
  }
}

output "hq_private_ips" {
  value = [oci_core_instance.hq.*.private_ip]
}
output "hq_public_ips" {
  value = [oci_core_instance.hq.*.public_ip]
}

