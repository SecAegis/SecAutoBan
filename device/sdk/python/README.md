# SecAutoBan Python SDK

## 安装

```Shell
pip3 install SecAutoBan
```

## 样例

### 告警模块

```Python
from SecAutoBan import SecAutoBan

def alarm_analysis(ws_client):
    ws_client.send_alarm("127.1.0.3", "127.0.0.1", "NMAP 扫描")

sec_auto_ban = SecAutoBan(
    server_ip="127.0.0.1",
    server_port=8000,
    sk="sk-*****",
    client_type="alarm",
    alarm_analysis=alarm_analysis
)
sec_auto_ban.run()
```

### 封禁模块

```Python
from SecAutoBan import SecAutoBan

def block_ip(ip):
    if check_exist_ip(ip):
        return
    pass

def unblock_ip(ip):
    pass

def get_all_block_ip() -> list:
    ip_list = []
    return ip_list

def check_exist_ip(ip) -> bool:
    return ip in get_all_block_ip()

sec_auto_ban = SecAutoBan(
    server_ip="127.0.0.1",
    server_port=8000,
    sk="sk-*****",
    client_type="block",
    block_ip=block_ip,
    unblock_ip=unblock_ip,
    get_all_block_ip=get_all_block_ip,
    enable_cidr=False
)
sec_auto_ban.run()
```

## 参数说明

| 参数                     | 描述                                                           | 是否需要填写         |
|------------------------|--------------------------------------------------------------|----------------|
| server_ip              | 核心模块回连IP                                                     | 需要             |
| server_port            | 核心模块回连端口                                                     | 需要             |
| sk                     | 设备页面生成的密钥                                                    | 需要             |
| client_type            | 模块类型(`alarm`/`block`)                                        | 需要             |
| enable_cidr            | 封禁模块是否开启 `Cidr` 封禁，若开启`block_ip()`和`unblock_ip()`参数将传入`Cidr` | 可选，默认为 `False` |
| alarm_analysis         | 告警分析函数                                                       | `alarm`模块必填    |
| block_ip               | 封禁函数                                                         | `block`模块必填    |
| unblock_ip             | 解禁函数                                                         | `block`模块必填    |
| get_all_block_ip       | 获取设备中全部封禁IP函数                                                | `block`模块可选    |
| login_success_callback | 登陆成功回调                                                       | 可选             |

## SDK调用方法

### send_alarm()

告警设备向平台发送告警信息。

eg:

```python
def alarm_analysis(ws_client):
    ws_client.send_alarm("攻击IP", "被攻击资产", "攻击方式")
```

or:

```
sec_auto_ban.send_alarm("攻击IP", "被攻击资产", "攻击方式")
```

### send_notify()

向平台发送通知。

eg:

```python
sec_auto_ban.send_notify("封禁失败", "xxx设备无法连接服务器")
```

### send_sync()

封禁设备主动向平台请求全部封禁IP。常用于脚本第一次启动，需同步全量IP场景。

eg:

```python
def login_success_callback():
    sec_auto_ban.send_sync()
```
