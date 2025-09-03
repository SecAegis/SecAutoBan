import json
import base64
import requests
from SecAutoBan import SecAutoBan

requests.packages.urllib3.disable_warnings()


def get_token(data):
    if "?[" not in data:
        return "", data
    split_data = data.split("?[")[1].split("}?")
    return split_data[0], split_data[1]

def login():
    s = requests.session()
    url = fw_config["url"] + "/home/login/"
    post_data = {
        "name": fw_config["username"],
        "password": fw_config["password"],
        "pwdlen": fw_config["pwdlen"]
    }
    r = s.post(url, data=post_data, timeout=60, verify=False)
    token, data = get_token(r.text)
    if token == "":
        return None, "", ""
    authid = json.loads(base64.b64decode(data).decode("utf-8"))["data"]["authid"]
    return s, token, authid

def logout(session, userMark, token):
    url = fw_config["url"] + "/home/index/logout/?userMark=" + userMark + "&token=" + token
    headers = {
        "Referer": fw_config["url"] + "/html/webui/home.html?userMark=" + userMark
    }
    r = session.get(url, timeout=60, headers=headers, verify=False)


def block_ip(ip):
    s, token, userMark = login()
    if token == "":
        return
    token, exist_ip = check_exist_ip(s, userMark, token, ip)
    if exist_ip:
        return
    url = fw_config["url"] + "/home/default/blackListSpread/add/?userMark=" + userMark
    post_data = {
        "sip": ip,
        "sport": "",
        "dip": "",
        "dport": "",
        "l4_protocol": "",
        "@change": True,
        "commands[0][pf_blacklist_add][sip]": ip,
        "commands[0][pf_blacklist_add][sport]": "",
        "commands[0][pf_blacklist_add][dip]": "",
        "commands[0][pf_blacklist_add][dport]": "",
        "commands[0][pf_blacklist_add][l4_protocol]": "",
        "token": token
    }
    headers = {
        "Referer": fw_config["url"] + "/html/webui/home.html?userMark=" + userMark
    }
    r = s.post(url, data=post_data, headers=headers, timeout=60, verify=False)
    token, data = get_token(r.text)
    if "true" not in data:
        sec_auto_ban.print("[-] 添加封禁失败")
    logout(s, userMark, token)


def unblock_ip(ip):
    s, token, userMark = login()
    if token == "":
        return
    token, exist_ip = check_exist_ip(s, userMark, token, ip)
    if not exist_ip:
        return
    url = fw_config["url"] + "/home/default/blackListSpread/deleteLots/?userMark=" + userMark
    post_data = {
        "dataTuple[0][sip]": ip,
        "@change": True,
        "commands[0][pf_blacklist_delete][0][sip]" : ip,
        "commands[1][if]": False,
        "commands[2][if]": False,
        "commands[3][if]": False,
        "commands[4][if]": False,
        "token": token
    }
    headers = {
        "Referer": fw_config["url"] + "/html/webui/home.html?userMark=" + userMark
    }
    r = s.post(url, data=post_data, headers=headers, timeout=60, verify=False)
    token, data = get_token(r.text)
    if "true" not in data:
        sec_auto_ban.print("[-] 解除封禁失败")
    logout(s, userMark, token)


def check_exist_ip(session, userMark, token, ip):
    url = fw_config["url"] + "/home/default/blackListSpread/searchpf/?userMark=" + userMark + "&page=1&rows=30&search=" + ip + "&%40change=true&commands%5B0%5D%5Bpf_blacklist_static_search%5D%5B0%5D=" + ip + "&token=" + token
    headers = {
        "Referer": fw_config["url"] + "/html/webui/home.html?userMark=" + userMark
    }
    r = session.get(url, timeout=60, headers=headers, verify=False)
    new_token, data = get_token(r.text)
    if token == "":
        return token, False
    if json.loads(data)["total"] <= 0:
        return new_token, False
    return new_token, True


if __name__ == "__main__":
    fw_config = {
        "url": "https://xxx.xxx.xxx.xxx",
        "username": "xxxx",
        "password": "xxxx==",
        "pwdlen": 6
    }
    sec_auto_ban = SecAutoBan(
        server_ip="127.0.0.1",
        server_port=80,
        sk="sk-*****",
        client_type="block",
        block_ip=block_ip,
        unblock_ip=unblock_ip
    )
    sec_auto_ban.run()
