import os
from SecAutoBan import SecAutoBan


# 实现设备封禁函数
def block_ip(ip):
    pass


# 实现设备解封函数
def unblock_ip(ip):
    pass


if __name__ == "__main__":
    sec_auto_ban = SecAutoBan(
        server_ip=os.getenv("server_ip", "127.0.0.1"),
        server_port=int(os.getenv("server_port", 80)),
        sk=os.getenv("sk"),
        client_type="block",
        block_ip=block_ip,
        unblock_ip=unblock_ip,
        enable_cidr=False
    )
    sec_auto_ban.run()
