resource "oci_core_route_table" "route_table" {
  compartment_id = var.tenancy_ocid
  vcn_id         = oci_core_virtual_network.r0mk_vcn.id
  display_name   = "r0mkRouteTable"

  route_rules {
    destination       = "0.0.0.0/0"
    destination_type  = "CIDR_BLOCK"
    network_entity_id = oci_core_internet_gateway.internet_gateway.id
  }
}

