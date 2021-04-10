resource "oci_core_internet_gateway" "internet_gateway" {
  compartment_id = var.tenancy_ocid
  display_name   = "InternetGW"
  vcn_id         = oci_core_virtual_network.r0mk_vcn.id
}
