data "oci_identity_availability_domain" "ad" {
  compartment_id = var.tenancy_ocid
  ad_number      = 2
}

output "ad" {
  value = data.oci_identity_availability_domain.ad.name
}


