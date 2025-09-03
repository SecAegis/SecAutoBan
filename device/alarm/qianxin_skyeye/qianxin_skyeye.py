import json
import socketserver
from SecAutoBan import SecAutoBan


class SyslogUDPHandler(socketserver.DatagramRequestHandler):
    def __init__(self, request, client_address, server, ws_client):
        self.ws_client = ws_client
        super().__init__(request, client_address, server)
    def handle(self):
        data = self.request[0]
        if len(data) == 0:
            return
        message = data.decode('utf-8')
        msg = json.loads(message.split("|!alarm|!")[1])
        sip = msg["attack_sip"]
        if sip == "":
            return
        self.ws_client.send_alarm(sip, msg["alarm_sip"], "[" + msg["type"] + "]" + msg["vuln_type"])


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
