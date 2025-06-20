import ipaddress
import subprocess
from SecAutoBan import SecAutoBan


def check_cidr_type(cidr):
    network = ipaddress.ip_network(cidr, strict=False)
    if isinstance(network, ipaddress.IPv4Network):
        return "IPv4"
    elif isinstance(network, ipaddress.IPv6Network):
        return "IPv6"
    else:
        return "Unknown"


def block_ip(cidr):
    if check_exist_ip(cidr):
        return
    if check_cidr_type(cidr) == "IPv4":
        if cidr == "0.0.0.0/0":
            return
        subprocess.run(['gobgp', 'global', "rib", "add", cidr, "nexthop", nexthop_v4])
    elif check_cidr_type(cidr) == "IPv6":
        if cidr == "::/0":
            return
        subprocess.run(['gobgp', 'global', "rib", "add", cidr, "-a", "ipv6", "nexthop", nexthop_v6])


def unblock_ip(cidr):
    if check_cidr_type(cidr) == "IPv4":
        subprocess.run(['gobgp', 'global', "rib", "del", cidr])
    elif check_cidr_type(cidr) == "IPv6":
        subprocess.run(['gobgp', 'global', "rib", "del", cidr, "-a", "ipv6"])


def get_all_block_ip() -> list:
    ip_list = []
    result = subprocess.run(['gobgp', 'global', "rib"], capture_output=True, text=True)
    for i in result.stdout.split("\n")[1:]:
        if i == "":
            continue
        if nexthop_v4 not in i:
            continue
        ip_list.append(i.split(" ")[1])
    result = subprocess.run(['gobgp', 'global', "rib", "-a", "ipv6"], capture_output=True, text=True)
    for i in result.stdout.split("\n")[1:]:
        if i == "":
            continue
        if nexthop_v6 not in i:
            continue
        ip_list.append(i.split(" ")[1])
    return ip_list


def check_exist_ip(ip) -> bool:
    return ip in get_all_block_ip()


if __name__ == "__main__":
    nexthop_v4 = "192.0.0.253" # ipv4黑洞地址
    nexthop_v6 = "fc00::ac11:1/128" # ipv6黑洞地址
    sec_auto_ban = SecAutoBan(
        server_ip="127.0.0.1",
        server_port=80,
        sk="sk-*****",
        client_type="block",
        block_ip=block_ip,
        unblock_ip=unblock_ip,
        get_all_block_ip=get_all_block_ip,
        enable_cidr=True
    )
    sec_auto_ban.run()
    