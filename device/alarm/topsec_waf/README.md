# 天融信WAF

## 下载模块

```
wget https://raw.githubusercontent.com/SecAegis/SecAutoBan/main/device/alarm/topsec_waf/topsec_waf.py
```

## 安装依赖

```
pip3 install SecAutoBan
```

## 配置WAF

登录WAF后台，通过`系统管理`-`系统日志`-`日志服务器配置`，添加服务器。

![](./img/1.png)

服务器地址填写本模块运行的主机IP，端口可自定义配置，配置完成点击应用即可。

## 运行

```shell
server_ip=127.0.0.1 server_port=80 sk=sk-xxx listen_port=514 python3 topsec_waf.py
```

## 环境变量说明

| 变量名         | 样例        | 描述         |
|-------------|-----------|------------|
| server_ip   | 127.0.0.1 | 平台IP       |
| server_port | 80        | 平台端口       |
| sk          | sk-xxx    | 连接密钥       |
| listen_port | 514       | 监听Syslog端口 |
