# 启明星辰全网安全态势感知系统

## 下载模块

```shell
wget https://raw.githubusercontent.com/SecAegis/SecAutoBan/main/device/alarm/venustech_qwaqtsgzxt/venustech_qwaqtsgzxt.py
```

## 安装依赖

```shell
pip3 install SecAutoBan
```

## 配置全网安全态势感知系统

通过`联动响应`-`日志外发配置`，添加syslog推送。

![](./img/1.png)

新增一条配置，服务器IP为本脚本运行的服务器IP，传输方式选择UDP，配置选择特征检测即可。

## 运行

```shell
server_ip=127.0.0.1 server_port=80 sk=sk-xxx listen_port=514 python3 venustech_qwaqtsgzxt.py
```

## 环境变量说明

| 变量名         | 样例        | 描述         |
|-------------|-----------|------------|
| server_ip   | 127.0.0.1 | 平台IP       |
| server_port | 80        | 平台端口       |
| sk          | sk-xxx    | 连接密钥       |
| listen_port | 514       | 监听Syslog端口 |
