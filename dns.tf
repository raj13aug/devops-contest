data "google_dns_managed_zone" "env_dns_zone" {
  name = "my-cloudrroot7-domain-zone"
}


resource "google_dns_record_set" "default" {
  name         = "dora.${data.google_dns_managed_zone.env_dns_zone.dns_name}"
  managed_zone = data.google_dns_managed_zone.env_dns_zone.name
  type         = "A"
  ttl          = 300
  rrdatas = [
    google_compute_instance.demo.network_interface[0].access_config[0].nat_ip
  ]
}