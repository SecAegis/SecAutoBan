# 旁路阻断

本模块无需与其他封禁设备联动，将直接发送TCP Reset包实现封禁，仅适用于断开TCP连接。

当双向检测到封禁IP进行TCP握手时，模块将发送reset数据包强制关闭连接。

## 下载模块

```
wget https://raw.githubusercontent.com/sec-report/SecAutoBan/main/device/block/tcp_reset/tcp_reset.py
```

## 配置说明

### 安装依赖

```
pip3 install SecAutoBan scapy
```

### 配置模块

#### 修改回连核心模块配置

> 注意路由配置，不能从镜像网卡回连，可以通过封禁网卡回连。

更改脚本第`117`-`119`行

```
server_ip = "127.0.0.1",
server_port = 80,
sk = "sk-xxx",
```

#### 修改镜像网卡名称

> 旁路阻断方案需要镜像接收网络中全部流量进行分析，请配置镜像接口。

更改脚本第`112`行

```
sniff_iface = "eth0"
```

#### 修改封禁网卡名称

> 封禁网卡需能访问被阻断的设备，正常情况下直接接入交换即可。尽量接入到核心交换上，不然可能导致封禁不及时，漏掉数据包。

更改脚本第`113`行

```
reset_iface = "eth1"
```

## 运行

```shell
python3 tcp_reset.py
```
