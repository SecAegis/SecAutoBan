import os
import routeros_api
from SecAutoBan import SecAutoBan


def block_ip(ip):
    if check_exist_ip(ip):  # 防止重复封禁
        return
    connection = routeros_api.RouterOsApiPool(
        routeros_config["host"],
        port=routeros_config["port"],
        username=routeros_config["username"],
        password=routeros_config["password"],
        plaintext_login=routeros_config["plaintext_login"]
    )
    api = connection.get_api()
    address_list = api.get_resource('/ip/firewall/address-list')
    address_list.add(address=ip, list=routeros_config["list_name"])
    connection.disconnect()


def unblock_ip(ip):
    connection = routeros_api.RouterOsApiPool(
        routeros_config["host"],
        port=routeros_config["port"],
        username=routeros_config["username"],
        password=routeros_config["password"],
        plaintext_login=routeros_config["plaintext_login"]
    )
    api = connection.get_api()
    address_list = api.get_resource('/ip/firewall/address-list')
    ip_list = address_list.get(list="sec_auto_ban", address=ip)
    if len(ip_list) == 0:
        return
    address_list.remove(id=ip_list[0])
    connection.disconnect()


def get_all_block_ip() -> list:
    ip_list = []
    connection = routeros_api.RouterOsApiPool(
        routeros_config["host"],
        port=routeros_config["port"],
        username=routeros_config["username"],
        password=routeros_config["password"],
        plaintext_login=routeros_config["plaintext_login"]
    )
    api = connection.get_api()
    address_list = api.get_resource('/ip/firewall/address-list')
    for i in address_list.get(list="sec_auto_ban"):
        ip_list.append(i["address"])
    connection.disconnect()
    return ip_list


def check_exist_ip(ip) -> bool:
    connection = routeros_api.RouterOsApiPool(
        routeros_config["host"],
        port=routeros_config["port"],
        username=routeros_config["username"],
        password=routeros_config["password"],
        plaintext_login=routeros_config["plaintext_login"]
    )
    api = connection.get_api()
    address_list = api.get_resource('/ip/firewall/address-list')
    ip_list = address_list.get(list="sec_auto_ban", address=ip)
    connection.disconnect()
    if len(ip_list) == 0:
        return False
    return True


if __name__ == "__main__":
    routeros_config = {
        "host": os.getenv("ros_host", "10.0.0.1"),
        "port": int(os.getenv("ros_port", 8728)),
        "username": os.getenv("ros_username", "admin"),
        "password": os.getenv("ros_password", "xxx"),
        "plaintext_login": True if os.getenv("ros_plaintext_login", "true").lower() == "true" else False,
        "list_name": os.getenv("ros_list_name", "sec_auto_ban")
    }
    sec_auto_ban = SecAutoBan(
        server_ip=os.getenv("server_ip", "127.0.0.1"),
        server_port=int(os.getenv("server_port", 80)),
        sk=os.getenv("sk"),
        client_type="block",
        block_ip=block_ip,
        unblock_ip=unblock_ip,
        get_all_block_ip=get_all_block_ip
    )
    sec_auto_ban.run()
