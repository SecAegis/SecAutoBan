# 深信服防火墙

深信服防火墙封禁模块

## 下载模块

```
wget https://raw.githubusercontent.com/SecAegis/SecAutoBan/main/device/block/sangfor_firewall/sangfor_firewall.py
```

## 安装依赖

```
pip3 install SecAutoBan requests
```

## 配置深信服防火墙

添加API账号

#### 修改与深信服防火墙连接的地址

更改脚本第`103`行

```
"url": "http://xxx.xxx.xxx.xxx",
```

#### 填写深信服防火墙用户名密码

更改脚本第`104`-`105`行

```
"username": "xxx",
"password": "xxx",
```

## 运行

```shell
server_ip=127.0.0.1 server_port=80 sk=sk-xxx fw_url=http://xxx.xxx.xxx.xxx fw_username=api-admin fw_password=xxx python3 sangfor_firewall.py
```

## 环境变量说明

| 变量名         | 样例                     | 描述        |
|-------------|------------------------|-----------|
| server_ip   | 127.0.0.1              | 平台IP      |
| server_port | 80                     | 平台端口      |
| sk          | sk-xxx                 | 连接密钥      |
| fw_url      | http://xxx.xxx.xxx.xxx | 连接防火墙 URL |
| fw_username | api-admin              | 防火墙用户名    |
| fw_password | xxx                    | 防火墙密码     |
