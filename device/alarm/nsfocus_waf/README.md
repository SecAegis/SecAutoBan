# 绿盟WAF

## 下载模块

```shell
wget https://raw.githubusercontent.com/SecAegis/SecAutoBan/main/device/alarm/nsfocus_waf/nsfocus_waf.py
```

## 安装依赖

```shell
pip3 install SecAutoBan
```

## 配置说明

### 配置WAF

登录WAF后台，通过`日志报表`-`日志管理配置`-`Syslog配置`，添加服务器。

![](./img/1.jpg)

IP填写本模块运行的主机IP，端口可自定义配置：

![](./img/2.jpg)

配置完成点击保存即可。

## 运行

```shell
server_ip=127.0.0.1 server_port=80 sk=sk-xxx listen_port=514 python3 nsfocus_waf.py
```

## 环境变量说明

| 变量名         | 样例        | 描述         |
|-------------|-----------|------------|
| server_ip   | 127.0.0.1 | 平台IP       |
| server_port | 80        | 平台端口       |
| sk          | sk-xxx    | 连接密钥       |
| listen_port | 514       | 监听Syslog端口 |