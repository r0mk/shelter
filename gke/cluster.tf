resource "google_container_cluster" "primary" {
  name               = "r0mk-gke-cluster"
  location           = "europe-north1-a"
  remove_default_node_pool = true
  initial_node_count       = 1
  project = "ordinal-thinker-279006"


}

resource "google_container_node_pool" "primary_preemptible_nodes" {
  name       = "my-node-pool"
  project = "ordinal-thinker-279006"
  location   = "europe-north1-a"
  cluster    = google_container_cluster.primary.name
  node_count = 0

  node_config {
    preemptible  = true
    machine_type = "e2-small"

    metadata = {
      disable-legacy-endpoints = "true"
    }

    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}
