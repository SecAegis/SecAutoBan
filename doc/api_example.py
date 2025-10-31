import os
import time
import json
import requests
from Crypto.Cipher import AES

base_url = "http://127.0.0.1:8080"
ak = ""
sk = ""

headers = {
    "ak": ak
}


def encrypt_aes_gcm(data: bytes, sk: str) -> bytes:
    cipher = AES.new(sk.encode(), AES.MODE_GCM, nonce=(nonce:=os.urandom(12)))
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return nonce + ciphertext + tag


def decrypt_aes_gcm(data: bytes, sk: str) -> bytes:
    cipher = AES.new(sk.encode(), AES.MODE_GCM, nonce=data[:12])
    return cipher.decrypt_and_verify(data[12:-16], data[-16:])


# 获取已封禁的 IP / Cidr
def get_ban_ip_cidr(ip_cidr: str, page: int = 1, size: int = 100) -> str:
    post_data = {
        "ipCidr": ip_cidr,
        "page": page,
        "size": size
    }
    r = requests.post(base_url + "/api/ban", data=encrypt_aes_gcm(json.dumps(post_data).encode(), sk), headers=headers)
    if len(r.content) < 12:
        return ""
    return decrypt_aes_gcm(r.content, sk).decode()


# 封禁 IP / Cidr
def add_ban_ip_cidr(ip_cidr: str, expires_time: int = -1, attack_asset: str = "", attack_method: str = "", remark: str = "") -> bool:
    post_data = {
        "ipCidr": ip_cidr,
        "expiresTime": expires_time, # -1: 平台自动计算过期时间 | 0: 永不过期 | 毫秒级时间戳
        "attackAsset": attack_asset,
        "attackMethod": attack_method,
        "remark": remark
    }
    r = requests.put(base_url + "/api/ban", data=encrypt_aes_gcm(json.dumps(post_data).encode(), sk), headers=headers)
    if len(r.content) < 12:
        return False
    if json.loads(decrypt_aes_gcm(r.content, sk).decode())["status"] != "success":
        return False
    return True


# 更新封禁 IP / Cidr
def set_ban_ip_cidr(ip_cidr: str, expires_time: int = -1, attack_asset: str = "", attack_method: str = "", remark: str = "", status: bool = True) -> bool:
    post_data = {
        "ipCidr": ip_cidr,
        "expiresTime": expires_time,  # -1: 平台自动计算过期时间 | 0: 永不过期 | 毫秒级时间戳
        "attackAsset": attack_asset,
        "attackMethod": attack_method,
        "remark": remark,
        "status": status
    }
    r = requests.patch(base_url + "/api/ban", data=encrypt_aes_gcm(json.dumps(post_data).encode(), sk), headers=headers)
    if len(r.content) < 12:
        return False
    if json.loads(decrypt_aes_gcm(r.content, sk).decode())["status"] != "success":
        return False
    return True


# 删除封禁 IP / Cidr
def del_ban_ip_cidr(ip_cidr: str) -> bool:
    post_data = {
        "ipCidr": ip_cidr
    }
    r = requests.delete(base_url + "/api/ban", data=encrypt_aes_gcm(json.dumps(post_data).encode(), sk), headers=headers)
    if len(r.content) < 12:
        return False
    if json.loads(decrypt_aes_gcm(r.content, sk).decode())["status"] != "success":
        return False
    return True


# 获取已加白的 IP / Cidr
def get_white_ip_cidr(ip_cidr: str, page: int = 1, size: int = 100) -> str:
    post_data = {
        "ipCidr": ip_cidr,
        "page": page,
        "size": size
    }
    r = requests.post(base_url + "/api/whitelist", data=encrypt_aes_gcm(json.dumps(post_data).encode(), sk), headers=headers)
    if len(r.content) < 12:
        return ""
    return decrypt_aes_gcm(r.content, sk).decode()


# 加白 IP / Cidr
def add_white_ip_cidr(ip_cidr: str, expires_time: int = -1, _class: str = "", remark: str = "") -> bool:
    post_data = {
        "ipCidr": ip_cidr,
        "expiresTime": expires_time, # 0: 永不过期 | 毫秒级时间戳
        "class": _class,
        "remark": remark
    }
    r = requests.put(base_url + "/api/whitelist", data=encrypt_aes_gcm(json.dumps(post_data).encode(), sk), headers=headers)
    if len(r.content) < 12:
        return False
    if json.loads(decrypt_aes_gcm(r.content, sk).decode())["status"] != "success":
        return False
    return True


# 更新白名单 IP / Cidr
def set_white_ip_cidr(ip_cidr: str, expires_time: int = -1, _class: str = "", remark: str = "", status: bool = True) -> bool:
    post_data = {
        "ipCidr": ip_cidr,
        "expiresTime": expires_time,  # 0: 永不过期 | 毫秒级时间戳
        "class": _class,
        "remark": remark,
        "status": status
    }
    r = requests.patch(base_url + "/api/whitelist", data=encrypt_aes_gcm(json.dumps(post_data).encode(), sk), headers=headers)
    if len(r.content) < 12:
        return False
    if json.loads(decrypt_aes_gcm(r.content, sk).decode())["status"] != "success":
        return False
    return True


# 删除白名单 IP / Cidr
def del_white_ip_cidr(ip_cidr: str) -> bool:
    post_data = {
        "ipCidr": ip_cidr
    }
    r = requests.delete(base_url + "/api/whitelist", data=encrypt_aes_gcm(json.dumps(post_data).encode(), sk), headers=headers)
    if len(r.content) < 12:
        return False
    if json.loads(decrypt_aes_gcm(r.content, sk).decode())["status"] != "success":
        return False
    return True


if __name__ == "__main__":
    # 黑名单
    # 封禁前结果 -> 添加封禁 -> 封禁后结果 -> 更新已封禁参数 -> 更新后结果 -> 删除 -> 删除后结果
    print(get_ban_ip_cidr("0.0.0.0/0", page=1, size=100))
    print(add_ban_ip_cidr("3.3.3.3", -1, "测试资产", "测试攻击", "备注内容"))
    print(get_ban_ip_cidr("0.0.0.0/0", page=1, size=1))
    print(set_ban_ip_cidr("3.3.3.3", 0, "测试资产", "测试攻击", "备注内容", False))
    print(get_ban_ip_cidr("0.0.0.0/0", page=1, size=1))
    print(del_ban_ip_cidr("3.3.3.3"))
    print(get_ban_ip_cidr("", page=1, size=100))

    # 白名单
    # 加白前结果 -> 添加白名单 -> 加白后结果 -> 更新白名单参数 -> 更新后结果 -> 删除 -> 删除后结果
    print(get_white_ip_cidr("0.0.0.0/0", page=1, size=100))
    print(add_white_ip_cidr("8.8.8.8/8", int((time.time() + 60 * 60 * 24) * 1000) , "白名单类别", "备注内容"))
    print(get_white_ip_cidr("0.0.0.0/0", page=1, size=1))
    print(set_white_ip_cidr("8.8.8.8/8", 0, "白名单类别", "备注内容", False))
    print(get_white_ip_cidr("0.0.0.0/0", page=1, size=1))
    print(del_white_ip_cidr("8.8.8.8/8"))
    print(get_white_ip_cidr(""))



