resource "oci_core_security_list" "proxy_security_list" {
  compartment_id = var.tenancy_ocid
  vcn_id         = oci_core_virtual_network.r0mk_vcn.id
  display_name   = "sshSecurityList"

  egress_security_rules {
    protocol    = "6"
    destination = "0.0.0.0/0"
  }

  ingress_security_rules {
    protocol = "6"
    source   = "0.0.0.0/0"

    tcp_options {
      max = "23"
      min = "23"
    }
  }
}
