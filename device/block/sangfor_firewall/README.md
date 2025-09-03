# 深信服防火墙

深信服防火墙封禁模块

## 下载模块

```
wget https://raw.githubusercontent.com/SecAegis/SecAutoBan/main/device/block/sangfor_firewall/sangfor_firewall.py
```

## 配置深信服防火墙

添加API账号

## 配置模块

### 安装依赖

```
pip3 install SecAutoBan requests
```

### 修改配置

#### 修改回连核心模块配置

更改脚本第`108`-`110`行

```
server_ip = "127.0.0.1",
server_port = 80,
sk = "sk-xxx",
```

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
python3 sangfor_firewall.py
```
