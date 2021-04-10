provider "oci" {
  tenancy_ocid = var.tenancy_ocid
  user_ocid = var.user_ocid
  fingerprint = var.fingerprint
  private_key = var.private_key
  region = var.region
}

variable "tenancy_ocid" { type = string }
variable "user_ocid" { type = string }
variable "private_key" { type = string }
variable "fingerprint" { type = string }
variable "region" { type = string }
variable "public_key" { type = string }
