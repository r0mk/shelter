provider "google" {
  credentials = file("/home/r0mk/gke-r0mk.json")
  project     = ""
  version     = "~> 2.5.0"
}
