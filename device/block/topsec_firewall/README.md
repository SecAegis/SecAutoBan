# 天融信防火墙

天融信防火墙封禁模块

## 下载模块

```
wget https://raw.githubusercontent.com/SecAegis/SecAutoBan/main/device/block/topsec_firewall/topsec_firewall.py
```

## 配置天融信防火墙

需要关闭验证码登录

## 配置模块

### 安装依赖

```
pip3 install SecAutoBan requests
```

### 修改配置

#### 修改回连核心模块配置

更改脚本第`120`-`122`行

```
server_ip = "127.0.0.1",
server_port = 80,
sk = "sk-xxx",
```

#### 修改与天融信防火墙连接的地址

更改脚本第`114`行

```
"url": "http://xxx.xxx.xxx.xxx",
```

#### 填写天融信防火墙用户名密码

更改脚本第`115`-`117`行

```
"username": "xxx",
"password": "xxxxx==",
"pwdlen": 6
```

以上信息可通过登录页面抓包获取：

![](./img/1.png)

## 运行

```shell
python3 topsec_firewall.py
```
