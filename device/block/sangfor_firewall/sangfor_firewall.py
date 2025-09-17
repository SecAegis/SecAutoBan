import requests
from SecAutoBan import SecAutoBan
requests.packages.urllib3.disable_warnings()


def login() -> str:
    url = fw_config["url"] + "/api/v1/namespaces/@namespace/login"
    post_data = {
        "name": fw_config["username"],
        "password": fw_config["password"]
    }
    r = requests.post(url, json=post_data, timeout=60, verify=False)
    r = r.json()
    if r["message"] != "成功":
        sec_auto_ban.print("登录失败")
        return ""
    return r["data"]["loginResult"]["token"]


def logout(token):
    url = fw_config["url"] + "/api/v1/namespaces/@namespace/logout"
    post_data = {
        "loginResult": {
            "token": token
        }
    }
    requests.post(url, json=post_data, timeout=60, verify=False)


def block_ip(ip):
    token = login()
    if token == "":
        return
    if check_exist_ip(token, ip):
        logout(token)
        return
    url = fw_config["url"] + "/api/v1/namespaces/@namespace/whiteblacklist"
    post_data = {
        "type": "BLACK",
        "url": ip,
        "enable": True,
        "description": "联动封禁"
    }
    cookies = {
        "token": token
    }
    r = requests.post(url, json=post_data, cookies=cookies, timeout=60, verify=False)
    if "成功" not in r.text:
        sec_auto_ban.print("[-] 添加封禁失败")
    logout(token)


def unblock_ip(ip):
    token = login()
    if token == "":
        return
    if not check_exist_ip(token, ip):
        logout(token)
        return
    url = fw_config["url"] + "/api/v1/namespaces/@namespace/whiteblacklist/" + ip
    cookies = {
        "token": token
    }
    r = requests.delete(url, cookies=cookies, timeout=60, verify=False)
    if "成功" not in r.text:
        sec_auto_ban.print("[-] 解除封禁失败")
    logout(token)


def get_all_block_ip() -> list:
    all_ip_list = []
    token = login()
    if token == "":
        return []
    url = fw_config["url"] + "/api/v1/namespaces/@namespace/whiteblacklist?type=BLACK&_length=200"
    cookies = {
        "token": token
    }
    r = requests.get(url, cookies=cookies, timeout=60, verify=False)
    for i in range(r.json()["data"]["totalPages"]):
        for items in requests.get(url+"&_start=" + str(200 * i), cookies=cookies, timeout=60, verify=False).json()["data"]["items"]:
            if items["enable"] == False or items["type"] != "BLACK" or items["urlType"] != "ip":
                continue
            if items["url"] not in all_ip_list:
                all_ip_list.append(items["url"])
    logout(token)
    return all_ip_list


def check_exist_ip(token, ip) -> bool:
    url = fw_config["url"] + "/api/v1/namespaces/@namespace/whiteblacklist/" + ip
    cookies = {
        "token": token
    }
    r = requests.get(url, cookies=cookies, timeout=60, verify=False)
    if "不存在" in r.text:
        return False
    r = r.json()
    if r["data"]["enable"] == False or r["data"]["type"] != "BLACK":
        return False
    return True

if __name__ == "__main__":
    fw_config = {
        "url": "https://xxx.xxx.xxx.xxx",
        "username": "xxx",
        "password": "xxx",
    }
    sec_auto_ban = SecAutoBan(
        server_ip="127.0.0.1",
        server_port=80,
        sk="sk-*****",
        client_type="block",
        block_ip=block_ip,
        unblock_ip=unblock_ip,
        get_all_block_ip=get_all_block_ip
    )
    sec_auto_ban.run()
