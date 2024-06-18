#!/bin/bash

# VPN configuration variables
VPN_HOST="200.2.198.226"
VPN_PORT="11443"
VPN_USERNAME="ctr_cctv"
VPN_PASSWORD="cctv.,ctr24"

# Create openfortivpn configuration file
cat <<EOF > /etc/openfortivpn/config
host = $VPN_HOST
port = $VPN_PORT
username = $VPN_USERNAME
password = $VPN_PASSWORD
trusted-cert = "sha256:your_cert_fingerprint_here"  # optional, based on your VPN server configuration
EOF

# Run openfortivpn
openfortivpn -c /etc/openfortivpn/config
