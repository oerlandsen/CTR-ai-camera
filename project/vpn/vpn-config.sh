#!/bin/bash

# VPN configuration variables
VPN_HOST="200.2.198.226"
VPN_PORT="11443"
VPN_USERNAME="ctr_cctv"
VPN_PASSWORD="cctv.,ctr24"
VPN_TRUSTED_CERT="42dc5002f823d9373d46aaf05c342f13fbb8e883d5ada48fc147b3bd322687e0"

# Create openfortivpn configuration file
cat <<EOF > /etc/openfortivpn/config
host = $VPN_HOST
port = $VPN_PORT
username = $VPN_USERNAME
password = $VPN_PASSWORD
trusted-cert = $VPN_TRUSTED_CERT
EOF

# Run openfortivpn
openfortivpn -c /etc/openfortivpn/config