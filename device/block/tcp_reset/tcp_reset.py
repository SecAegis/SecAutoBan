import os
import random
import sqlite3
from SecAutoBan import SecAutoBan
from scapy.all import sniff, send
from scapy.layers.inet6 import IPv6
from scapy.layers.inet import TCP, IP
from multiprocessing.pool import ThreadPool


def get_ip(p):
    src_ip = ""
    dst_ip = ""
    if p.haslayer(IP):
        src_ip = p[IP].src
        dst_ip = p[IP].dst
    if p.haslayer(IPv6):
        src_ip = p[IPv6].src
        dst_ip = p[IPv6].dst
    return src_ip, dst_ip


def send_reset(iface):
    def f(p):
        src_ip, dst_ip = get_ip(p)
        src_port = p[TCP].sport
        dst_port = p[TCP].dport
        ack = p[TCP].ack
        if "S" in p[TCP].flags:
            return
        try:
            if p.haslayer(IP):
                p = IP(src=dst_ip, dst=src_ip) / TCP(sport=dst_port, dport=src_port, flags="R", window=2052, seq=ack)
                send(p, verbose=0, iface=iface)
                return
            if p.haslayer(IPv6):
                p = IPv6(src=dst_ip, dst=src_ip) / TCP(sport=dst_port, dport=src_port, flags="R", window=2052, seq=ack)
                send(p, verbose=0, iface=iface)
                return
        except Exception as e:
            pass
    return f


def is_filter():
    def f(p):
        if not p.haslayer(TCP):
            return False
        src_ip, dst_ip = get_ip(p)
        return src_ip in ban_ip_list or dst_ip in ban_ip_list
    return f


def get_db_all_ip():
    db_ip_list = []
    with sqlite3.connect(db_name) as sql_conn:
        cursor = sql_conn.cursor().execute("SELECT ip from IP")
        for row in cursor:
            db_ip_list.append(row[0])
    return db_ip_list


def block_ip(ip):
    if check_exist_ip(ip):
        return
    global ban_ip_list
    ban_ip_list.append(ip)
    with sqlite3.connect(db_name) as sql_conn:
        sql_conn.execute('INSERT INTO IP (ip) VALUES (?)', (ip,))
        sql_conn.commit()


def unblock_ip(ip):
    global ban_ip_list
    ban_ip_list.remove(ip)
    with sqlite3.connect(db_name) as sql_conn:
        sql_conn.execute('DELETE FROM IP WHERE ip=?', (ip,))
        sql_conn.commit()


def get_all_block_ip() -> list:
    return ban_ip_list


def check_exist_ip(ip) -> bool:
    return ip in ban_ip_list


def run_sniff():
    with sqlite3.connect(db_name) as sql_conn:
        sql_conn.execute('''
            CREATE TABLE IF NOT EXISTS IP (
                ip TEXT,
                CONSTRAINT idx_ip UNIQUE (ip)
            )
        ''')
    global ban_ip_list
    ban_ip_list.clear()
    ban_ip_list += get_db_all_ip()
    sniff(
        iface=sniff_iface,
        prn=send_reset(reset_iface),
        lfilter=is_filter()
    )


if __name__ == "__main__":
    sniff_iface = os.getenv("sniff_iface", "eth0")
    reset_iface = os.getenv("reset_iface", "eth1")
    db_name = "block_ip.db"
    ban_ip_list = []
    sec_auto_ban = SecAutoBan(
        server_ip=os.getenv("server_ip", "127.0.0.1"),
        server_port=int(os.getenv("server_port", 80)),
        sk=os.getenv("sk"),
        client_type="block",
        block_ip=block_ip,
        unblock_ip=unblock_ip,
        get_all_block_ip=get_all_block_ip
    )
    pool = ThreadPool(processes=1)
    sec_auto_ban.print("[*] 开始拦截")
    pool.apply_async(run_sniff)
    pool.close()
    sec_auto_ban.run()
    pool.join()
