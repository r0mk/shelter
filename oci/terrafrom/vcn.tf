resource "oci_core_virtual_network" "r0mk_vcn" {
  cidr_block     = "10.10.0.0/16"
  display_name   = "r0mk-VCN-net"
  dns_label      = "r0mkvcn"
  compartment_id = var.tenancy_ocid
}
