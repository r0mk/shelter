resource "oci_core_instance" "arm" {
  availability_domain =  data.oci_identity_availability_domain.ad.name
  compartment_id      = var.tenancy_ocid
  display_name        = "arm"
  shape               = "VM.Standard.A1.Flex"
  shape_config {
    memory_in_gbs = 24
    ocpus = 4
  }
  create_vnic_details {
    subnet_id        = oci_core_subnet.oci_subnet.id
    display_name     = "primaryvnic"
    assign_public_ip = true
    hostname_label   = "arm"
  }

  source_details {
    source_type = "image"
    #source_id   = data.oci_core_image.ubuntu_2004_min.id
    #source_id   = "ocid1.image.oc1.eu-frankfurt-1.aaaaaaaala3albkmkwmgkpbe5nkbfwmhjw74e4yzzrzrvwe7tgalsblataua"
    source_id   = "ocid1.image.oc1.eu-frankfurt-1.aaaaaaaapzfowmk3dwyurhox53yx4eqkmwourxs2ujxgykiymgsw4xnmmkya"

 }

  metadata = {
    ssh_authorized_keys = var.public_key
  }
}

output "arm_private_ips" {
  value = [oci_core_instance.arm.*.private_ip]
}
output "arm_public_ips" {
  value = [oci_core_instance.arm.*.public_ip]
}

