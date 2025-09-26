# BGP封禁

通过BGP协议，对需封禁的IP设置黑洞路由（需路由器支持）。

## 下载模块

```shell
wget https://raw.githubusercontent.com/SecAegis/SecAutoBan/main/device/block/bgp/bgp.py
```

## 安装依赖

```shell
pip3 install SecAutoBan
```


## 配置BGP

需要在Agent上运行[GOBGP](https://github.com/osrg/gobgp)服务

### 安装GOBGP

```shell
# 下载
curl -L -o gobgp.tar.gz $(curl -s https://api.github.com/repos/osrg/gobgp/releases/latest | grep browser_download_url | cut -d'"' -f4 | grep amd64)

# 解压至/usr/bin
tar -xzf gobgp.tar.gz -C /usr/bin gobgp gobgpd && rm gobgp.tar.gz

# 配置文件
# 目前 run.sh 会自动生成配置文件
# 配置文件手册: https://github.com/osrg/gobgp/blob/master/docs/sources/configuration.md
```

## 运行

```shell
server_ip=127.0.0.1 server_port=80 sk=sk-xxx nexthop_v4=192.0.0.253 nexthop_v6=fc00::ac11:1/128 as=65551 local_ip=10.0.0.2 neighbor_ip=10.0.0.1 sh run.sh
```

## 环境变量说明

| 变量名         | 样例               | 描述                 |
|-------------|------------------|--------------------|
| server_ip   | 127.0.0.1        | 平台IP               |
| server_port | 80               | 平台端口               |
| sk          | sk-xxx           | 连接密钥               |
| nexthop_v4  | 192.0.0.253      | ipv4黑洞地址           |
| nexthop_v6  | fc00::ac11:1/128 | ipv6黑洞地址           |
| as          | 65551            | BGP自治系统AS号         |
| local_ip    | 10.0.0.2         | 当前主机IP             |
| neighbor_ip | 10.0.0.1         | BGP邻居IP（向该BGP同步路由） |

