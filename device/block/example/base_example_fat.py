from SecAutoBan import SecAutoBan

# 实现设备封禁函数
def block_ip(ip):
    if check_exist_ip(ip):  # 防止重复封禁
        return
    pass


# 实现设备解封函数
def unblock_ip(ip):
    pass


# 实现获取全量已封禁IP函数
def get_all_block_ip() -> list:
    ip_list = []
    return ip_list


# 若有更快速方法，请重新实现查询设备是否已封禁IP函数，返回True为已封禁，返回False为未封禁
def check_exist_ip(ip) -> bool:
    return ip in get_all_block_ip()

# 第一次运行并登陆成功后，同步全量封禁IP至封禁设备（可选）
def login_success_callback():
    global init
    if init == 0:
        sec_auto_ban.send_sync()
        init += 1

if __name__ == "__main__":
    init = 0
    sec_auto_ban = SecAutoBan(
        server_ip="127.0.0.1",
        server_port=80,
        sk="sk-*****",
        client_type="block",
        block_ip=block_ip,
        unblock_ip=unblock_ip,
        get_all_block_ip=get_all_block_ip,
        login_success_callback=login_success_callback,
        enable_cidr=False
    )
    sec_auto_ban.run()
