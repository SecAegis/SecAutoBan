import json
import socketserver
from SecAutoBan import SecAutoBan


class SyslogTCPHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server, ws_client):
        self.ws_client = ws_client
        super().__init__(request, client_address, server)
    def handle(self):
        buffer = b""
        with self.request.makefile('rb') as f:
            for chunk in f:
                buffer += chunk
                parts = buffer.split(b"\x00")
                buffer = parts.pop()
                for line in parts:
                    line = line.strip()
                    if not line:
                        continue
                    sub_parts = line.split(b"|!")
                    if len(sub_parts) <= 3:
                        continue
                    try:
                        msg = json.loads(sub_parts[3])
                        self.ws_client.send_alarm(msg["attack_ip"], msg["suffer_ip"], msg["event_desc"])
                    except Exception as e:
                        pass


def alarm_analysis(ws_client):
    with socketserver.ThreadingTCPServer(("0.0.0.0", listen_syslog_tcp_port), lambda *args: SyslogTCPHandler(*args, ws_client=ws_client)) as server:
        sec_auto_ban.print("[+] 监听SysLog端口: " + str(listen_syslog_tcp_port) + "/TCP")
        server.serve_forever()


if __name__ == "__main__":
    listen_syslog_tcp_port = 567
    sec_auto_ban = SecAutoBan(
        server_ip="127.0.0.1",
        server_port=80,
        sk="sk-*****",
        client_type="alarm",
        alarm_analysis = alarm_analysis
    )
    sec_auto_ban.run()
