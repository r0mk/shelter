resource "oci_core_security_list" "proxy_security_list" {
  compartment_id = var.tenancy_ocid
  vcn_id         = oci_core_virtual_network.r0mk_vcn.id
  display_name   = "sshSecurityList"

  egress_security_rules {
    protocol    = "6"
    destination = "0.0.0.0/0"
  }

  ingress_security_rules {
    protocol    = "1" 
    source      = "91.146.50.0/24"
    source_type = "CIDR_BLOCK"
    stateless   = false 
  }

  ingress_security_rules {
    protocol = "6"
    source   = "91.146.50.0/24"
    tcp_options {
      max = "22"
      min = "22"
    }
  }

  ingress_security_rules {
    protocol = "6"
    source   = "0.0.0.0/0"
    tcp_options {
      max = "33128"
      min = "33128"
    }
  }

  ingress_security_rules {
    protocol = "17"
    source   = "0.0.0.0/0"
    udp_options {
      max = "1194"
      min = "1194"
    }
  }



}
