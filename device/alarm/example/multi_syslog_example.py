import socket
import socketserver
from threading import Lock, Timer


def reset_count():
    global message_count
    if len(message_count) != 0:
        message = "[*] 过去1小时转发syslog:"
        for i in message_count:
            message += " [" + i + "]" + str(message_count[i]) + "条"
        print(message)
        with message_count_lock:
            message_count = {}
    Timer(3600, reset_count).start()


def add_count(device_name):
    global message_count
    with message_count_lock:
        if device_name not in message_count:
            message_count[device_name] = 1
        else:
            message_count[device_name] += 1

class SyslogUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].split(b' ')
        if len(data) < 7:
            return
        if data[7] == b"xxx1":
            socket.socket(socket.AF_INET, socket.SOCK_DGRAM).sendto(b''.join(data[7:]), ("127.0.0.1", 515))
            add_count("xxx1")
        elif data[7] == b"xxx2":
            socket.socket(socket.AF_INET, socket.SOCK_DGRAM).sendto(b''.join(data[7:]), ("127.0.0.1", 516))
            add_count("xxx2")
        else:
            pass


if __name__ == "__main__":
    message_count = {}
    message_count_lock = Lock()
    listen_syslog_udp_port = 514
    with socketserver.ThreadingUDPServer(("0.0.0.0", listen_syslog_udp_port), lambda *args: SyslogUDPHandler(*args)) as server:
        print("[+] 监听SysLog端口: " + str(listen_syslog_udp_port) + "/UDP")
        reset_count()
        server.serve_forever()
