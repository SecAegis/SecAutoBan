import os
import time
from SecAutoBan import SecAutoBan

# 实现解析设备log函数，最后调用send_alarm_ip("攻击ip", "受害IP","备注")向服务器发送告警IP
def alarm_analysis(ws_client):
    while True:
        time.sleep(1)
        ws_client.send_alarm("127.1.0.3", "127.0.0.1","NMAP 扫描")


if __name__ == "__main__":
    sec_auto_ban = SecAutoBan(
        server_ip=os.getenv("server_ip", "127.0.0.1"),
        server_port=int(os.getenv("server_port", 80)),
        sk=os.getenv("sk"),
        client_type="alarm",
        alarm_analysis = alarm_analysis
    )
    sec_auto_ban.run()
