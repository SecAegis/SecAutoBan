import socket
import socketserver


class SyslogUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].split(b' ')
        if len(data) < 7:
            return
        if data[7] == "xxx1":
            socket.socket(socket.AF_INET, socket.SOCK_DGRAM).sendto(b''.join(data[7:]), ("127.0.0.1", 515))
        elif data[7] == "xxx2":
            socket.socket(socket.AF_INET, socket.SOCK_DGRAM).sendto(b''.join(data[7:]), ("127.0.0.1", 516))
        else:
            pass

if __name__ == "__main__":
    listen_syslog_udp_port = 514
    with socketserver.ThreadingUDPServer(("0.0.0.0", listen_syslog_udp_port), lambda *args: SyslogUDPHandler(*args)) as server:
        print("[+] 监听SysLog端口: " + str(listen_syslog_udp_port) + "/UDP")
        server.serve_forever()