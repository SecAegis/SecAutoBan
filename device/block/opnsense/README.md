# OPNsense

OPNsense封禁

## 下载模块

```shell
wget https://raw.githubusercontent.com/SecAegis/SecAutoBan/main/device/block/opnsense/opnsense.py
```

## 安装依赖

```shell
pip3 install SecAutoBan requests
```

## 配置OPNsense

### 添加API

查看[官方文档](https://docs.opnsense.org/development/how-tos/api.html)为用户添加API密钥

### 创建别名组

在`防火墙-别名`页面新建别名`sec_auto_ban`并保存:

![](./img/1.jpg)

### 为别名组创建封禁规则

在`防火墙-规则-浮动`页面新建两条规则，分别为阻止源IP为别名组及目标IP为别名组，图例:

![](./img/2.jpg)

## 运行

```shell
server_ip=127.0.0.1 server_port=80 sk=sk-xxx opensense_url=http://xxx.xxx.xxx.xxx opensense_api_key=xxx opensense_api_secret=xxx opensense_alias_name=sec_auto_ban python3 opnsense.py
```

## 环境变量说明

| 变量名                  | 样例                     | 描述               |
|----------------------|------------------------|------------------|
| server_ip            | 127.0.0.1              | 平台IP             |
| server_port          | 80                     | 平台端口             |
| sk                   | sk-xxx                 | 连接密钥             |
| opensense_url        | http://xxx.xxx.xxx.xxx | 连接 OPNsense URL  |
| opensense_api_key    | xxx                    | OPNsense API Key |
| opensense_api_secret | xxx                    | OPNsense API 密钥  |
| opensense_alias_name | sec_auto_ban           | 防火墙别名            |
