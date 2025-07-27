from . import util
from multiprocessing.pool import ThreadPool
from .websocket_client import WebSocketClient

class SecAutoBan:
    init = False
    main_thread_pool_processes = 1
    
    def __init__(self, server_ip, server_port, sk, client_type, enable_cidr=False, alarm_analysis=None, block_ip=None, unblock_ip=None, get_all_block_ip=None, login_success_callback=None):
        self.client_type = client_type
        if client_type == "alarm":
            if alarm_analysis is None:
                util.print("[-] 初始化失败: 未实现告警函数")
                return
            self.alarm_analysis = alarm_analysis
            self.main_thread_pool_processes += 1
        if self.client_type == "block":
            if block_ip is None:
                util.print("[-] 初始化失败: 未实现封禁函数")
                return
            if unblock_ip is None:
                util.print("[-] 初始化失败: 未实现解封函数")
                return
        self.ws_client = WebSocketClient(server_ip, server_port, sk, client_type, enable_cidr, block_ip, unblock_ip, get_all_block_ip, login_success_callback)
        self.init = True

    def print(self, message):
        util.print(message)

    def send_alarm(self, ip: str, attack_asset: str, attack_method: str):
        self.ws_client.send_alarm(ip, attack_asset, attack_method)

    def send_notify(self, title: str, content: str):
        self.ws_client.send_notify(title, content)

    def send_sync(self):
        self.ws_client.send_sync()

    def run(self):
        if not self.init:
            return
        pool = ThreadPool(processes=self.main_thread_pool_processes)
        if self.client_type == "alarm":
            pool.apply_async(self.alarm_analysis, args=(self.ws_client,))
        pool.apply_async(self.ws_client.connect)
        pool.close()
        pool.join()
        