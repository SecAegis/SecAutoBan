import json
import socketserver
from SecAutoBan import SecAutoBan


class SyslogUDPHandler(socketserver.DatagramRequestHandler):
    def __init__(self, request, client_address, server, ws_client):
        self.ws_client = ws_client
        super().__init__(request, client_address, server)
    def handle(self):
        data = self.request[0]
        if len(data.split(b" respond:")) < 2:
            return
        data = json.loads(data.split(b" respond:")[1].decode())
        src_ip = data["src_ip"]
        if src_ip == "":
            src_ip = data["src_ip_v6"]
        dst_ip = data["dst_ip"]
        if dst_ip == "":
            dst_ip = data["dst_ip_v6"]
        event_type = data["subject"]
        self.ws_client.send_alarm(src_ip, dst_ip, event_type)


def alarm_analysis(ws_client):
    with socketserver.ThreadingUDPServer(("0.0.0.0", listen_syslog_udp_port), lambda *args: SyslogUDPHandler(*args, ws_client=ws_client)) as server:
        sec_auto_ban.print("[+] 监听SysLog端口: " + str(listen_syslog_udp_port) + "/UDP")
        server.serve_forever()


if __name__ == "__main__":
    listen_syslog_udp_port = 567
    sec_auto_ban = SecAutoBan(
        server_ip="127.0.0.1",
        server_port=80,
        sk="sk-*****",
        client_type="alarm",
        alarm_analysis = alarm_analysis
    )
    sec_auto_ban.run()
