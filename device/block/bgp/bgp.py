import socket
import subprocess
from SecAutoBan import SecAutoBan


def check_ip_version(ip):
    try:
        socket.inet_pton(socket.AF_INET, ip)
        return "IPv4"
    except socket.error:
        try:
            socket.inet_pton(socket.AF_INET6, ip)
            return "IPv6"
        except socket.error:
            return "Invalid IP"


def block_ip(ip):
    if check_exist_ip(ip):
        return
    prefix = "/32"
    if (ip_version := check_ip_version(ip)) == "IPv6":
        prefix = "/128"
    elif ip_version == "Invalid IP":
        return
    subprocess.run(['gobgp', 'global', "rib", "add", ip + prefix, "nexthop", nexthop])


def unblock_ip(ip):
    prefix = "/32"
    if (ip_version := check_ip_version(ip)) == "IPv6":
        prefix = "/128"
    elif ip_version == "Invalid IP":
        return
    subprocess.run(['gobgp', 'global', "rib", "del", ip + prefix])


def get_all_block_ip() -> list:
    ip_list = []
    result = subprocess.run(['gobgp', 'global', "rib"], capture_output=True, text=True)
    for i in result.stdout.split("\n")[1:]:
        if i == "":
            continue
        if nexthop not in i:
            continue
        ip_list.append(i.split(" ")[1].split("/")[0])
    return ip_list


def check_exist_ip(ip) -> bool:
    return ip in get_all_block_ip()


if __name__ == "__main__":
    nexthop = "192.0.2.1" # 黑洞地址
    sec_auto_ban = SecAutoBan(
        server_ip="127.0.0.1",
        server_port=80,
        sk="sk-*****",
        client_type="block",
        block_ip = block_ip,
        unblock_ip = unblock_ip,
        get_all_block_ip= get_all_block_ip
    )
    sec_auto_ban.run()
    