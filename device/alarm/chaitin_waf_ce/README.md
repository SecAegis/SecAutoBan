# 长亭WAF社区版

长亭WAF社区版非专业版没有Syslog权限，采用前端轮询的方式获取告警数据。

![](./img/1.jpg)

## 下载模块

```
wget https://raw.githubusercontent.com/SecAegis/SecAutoBan/main/device/alarm/chaitin_waf_ce/chaitin_waf_ce.py
```

## 配置说明

### 安装依赖

```
pip3 install SecAutoBan requests
```

### 配置模块

#### 修改回连核心模块配置

更改脚本第`36`-`38`行

```
server_ip = "127.0.0.1",
server_port = 80,
sk = "sk-xxx",
```

#### 修改与WAF连接的地址

更改脚本第`32`行

```
"url": "https://xxx.xxx.xxx.xxx:9443",
```

#### 修改登录配置

登录WAF管理界面，在`系统设置`-`API Token`处生成Token并复制

![](./img/api.jpg)

将Token填写在脚本第`33`行

```
chaitin_waf_config = {
    "url": "https://xxx.xxx.xxx.xxx:9443",
    "apikey": "xxxxxxx",  # <-填写这个字段
}
```

## 运行

```shell
python3 chaitin_waf_ce.py
```
