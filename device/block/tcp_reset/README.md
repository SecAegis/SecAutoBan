# 旁路阻断

本模块无需与其他封禁设备联动，将直接发送TCP Reset包实现封禁，仅适用于断开TCP连接。

当双向检测到封禁IP进行TCP握手时，模块将发送reset数据包强制关闭连接。

## 下载模块

```shell
wget https://raw.githubusercontent.com/SecAegis/SecAutoBan/main/device/block/tcp_reset/tcp_reset.py
```
## 安装依赖

```shell
pip3 install SecAutoBan scapy
```

## 运行

```shell
server_ip=127.0.0.1 server_port=80 sk=sk-xxx sniff_iface=eth0 reset_iface=eth1 python3 tcp_reset.py
```

## 环境变量说明

| 变量名         | 样例        | 描述                                |
|-------------|-----------|-----------------------------------|
| server_ip   | 127.0.0.1 | 平台IP                              |
| server_port | 80        | 平台端口                              |
| sk          | sk-xxx    | 连接密钥                              |
| sniff_iface | eth0      | 镜像网卡名称，旁路阻断方案需要镜像接收网络中全部流量进行分析    |
| reset_iface | eth1      | 封禁网卡名称，需能访问被阻断的设备，正常情况下直接接入核心交换即可 |