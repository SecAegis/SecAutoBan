if [ ! -d "/etc/gobgp" ]; then
  mkdir /etc/gobgp
fi
if [ ! -f "/etc/gobgp/gobgpd.conf" ]; then
    cat > /etc/gobgp/gobgpd.conf << EOF
[global.config]
as = $as
router-id = "$local_ip"

[[neighbors]]
[neighbors.config]
  neighbor-address = "$neighbor_ip"
  peer-as = $as

[[neighbors.afi-safis]]
  [neighbors.afi-safis.config]
  afi-safi-name = "ipv4-unicast"

[[neighbors.afi-safis]]
  [neighbors.afi-safis.config]
  afi-safi-name = "ipv6-unicast"
EOF
fi
/usr/bin/gobgpd -f /etc/gobgp/gobgpd.conf & python3 /device/block/bgp/bgp.py
