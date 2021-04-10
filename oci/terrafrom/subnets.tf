resource "oci_core_subnet" "oci_subnet" {
  cidr_block        = "10.10.0.0/24"
  display_name      = "ociSubnet"
  dns_label         = "ocisubnet"
  vcn_id            = oci_core_virtual_network.r0mk_vcn.id
  route_table_id    = oci_core_route_table.route_table.id
  #dhcp_options_id   = oci_core_virtual_network.test_vcn.default_dhcp_options_id
  compartment_id = var.tenancy_ocid
  security_list_ids = [ oci_core_security_list.proxy_security_list.id ]

}
