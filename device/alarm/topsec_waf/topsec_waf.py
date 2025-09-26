import os
import socketserver
from SecAutoBan import SecAutoBan


class SyslogUDPHandler(socketserver.DatagramRequestHandler):
    def __init__(self, request, client_address, server, ws_client):
        self.ws_client = ws_client
        super().__init__(request, client_address, server)
    def handle(self):
        data = self.request[0]
        if b' action="deny" ' not in data:
            return
        src_ip = ""
        dst_ip = ""
        event_type = ""
        for i in data.split(b" "):
            if i[:9] == b'real_ip="':
                src_ip = i[9:-1].decode()
                continue
            if i[:11] == b'server_ip="':
                dst_ip = i[11:-1].decode()
                continue
            if i[:12] == b'event_type="':
                event_type = i[12:-1].decode()
            if src_ip != "" and dst_ip != "" and event_type != "":
                break
        self.ws_client.send_alarm(src_ip, dst_ip, event_type)


def alarm_analysis(ws_client):
    with socketserver.ThreadingUDPServer(("0.0.0.0", listen_syslog_udp_port), lambda *args: SyslogUDPHandler(*args, ws_client=ws_client)) as server:
        sec_auto_ban.print("[+] 监听SysLog端口: " + str(listen_syslog_udp_port) + "/UDP")
        server.serve_forever()


if __name__ == "__main__":
    listen_syslog_udp_port = int(os.getenv("listen_port", 514))
    sec_auto_ban = SecAutoBan(
        server_ip=os.getenv("server_ip", "127.0.0.1"),
        server_port=int(os.getenv("server_port", 80)),
        sk=os.getenv("sk"),
        client_type="alarm",
        alarm_analysis = alarm_analysis
    )
    sec_auto_ban.run()
