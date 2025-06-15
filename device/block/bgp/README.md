# BGP封禁

通过BGP协议，对需封禁的IP设置黑洞路由（需路由器支持）。

## 下载模块

```
wget https://raw.githubusercontent.com/SecAegis/SecAutoBan/main/device/block/bgp/bgp.py
```

## 配置BGP

需要在Agent上运行[GOBGP](https://github.com/osrg/gobgp)服务

### 安装GOBGP

```shell
# 下载
curl -L -o gobgp.tar.gz $(curl -s https://api.github.com/repos/osrg/gobgp/releases/latest | grep browser_download_url | cut -d'"' -f4 | grep amd64)

# 解压至/usr/bin
tar -xzf gobgp.tar.gz -C /usr/bin gobgp gobgpd && rm gobgp.tar.gz

# 生成配置文件
# 配置文件手册: https://github.com/osrg/gobgp/blob/master/docs/sources/configuration.md
mkdir /etc/gobgp
cat << EOF > /etc/gobgp/gobgpd.conf
[global.config]
  as = 65551
  router-id = "192.168.0.2"

[[neighbors]]
  [neighbors.config]
    neighbor-address = "192.168.0.1"
    peer-as = 65551
EOF

# 添加为服务并启动
cat << EOF > /etc/systemd/system/gobgpd.service
[Unit]
Description=GOBGP Server Service
After=network.target

[Service]
Type=simple
User=root
Restart=on-failure
RestartSec=5s
ExecStart=/usr/bin/gobgpd -f /etc/gobgp/gobgpd.conf

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable gobgpd
systemctl start gobgpd
```

## 配置模块

### 安装依赖

```
pip3 install SecAutoBan
```

### 修改配置

#### 修改黑洞地址

更改脚本第`43`-`44`行

```python
nexthop_v4 = "192.0.0.253" # ipv4黑洞地址
nexthop_v6 = "fc00::ac11:1/128" # ipv6黑洞地址
```

#### 修改回连核心模块配置

更改脚本第`46`-`48`行

```python
server_ip = "127.0.0.1",
server_port = 80,
sk = "sk-xxx",
```

## 运行

```shell
python3 bgp.py
```
