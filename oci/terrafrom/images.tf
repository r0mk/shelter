data "oci_core_images" "ubuntu_2004_min_search" {
    compartment_id = var.tenancy_ocid
    display_name = "Canonical-Ubuntu-20.04-Minimal-2021.03.25-0"
}

data "oci_core_image" "ubuntu_2004_min" {
    image_id = data.oci_core_images.ubuntu_2004_min_search.images.0.id
}
