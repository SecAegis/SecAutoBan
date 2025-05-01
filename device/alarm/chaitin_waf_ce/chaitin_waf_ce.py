import time
import requests
from SecAutoBan import SecAutoBan
requests.packages.urllib3.disable_warnings()

def alarm_analysis(ws_client):
    while True:
        time.sleep(5)
        try:
            r = requests.get(
                chaitin_waf_config["url"] + "/api/open/records?page=1&page_size=20&ip=&url=&port=&host=&attack_type=&action=1",
                headers={
                    "X-SLCE-API-TOKEN": chaitin_waf_config["apikey"]
                },
                verify=False
            )
        except Exception as e:
            sec_auto_ban.print("[-] WAF连接失败, Error: " + str(e))
            continue
        if r.status_code != 200:
            if r.status_code == 401:
                sec_auto_ban.print("[-] WAF登录失败")
                continue
            sec_auto_ban.print("[-] WAF连接失败")
            continue
        for i in r.json()["data"]["data"]:
            ws_client.send_alarm(i["src_ip"], i["host"], i["reason"])


if __name__ == "__main__":
    chaitin_waf_config = {
        "url": "https://xxx.xxx.xxx.xxx:9443",
        "apikey": ""
    }
    sec_auto_ban = SecAutoBan(
        server_ip="127.0.0.1",
        server_port=80,
        sk="sk-*****",
        client_type="alarm",
        alarm_analysis = alarm_analysis
    )
    sec_auto_ban.run()
