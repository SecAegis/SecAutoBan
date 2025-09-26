# 深信服态势感知


## 下载模块

```shell
wget https://raw.githubusercontent.com/SecAegis/SecAutoBan/main/device/alarm/sangfor_sip/sangfor_sip.py
```

## 安装依赖

```shell
pip3 install SecAutoBan
```

# 配置深信服态势感知

添加syslog推送，由于默认数据包过大，UDP存在截断问题，需选择TCP推送。

## 运行

```shell
server_ip=127.0.0.1 server_port=80 sk=sk-xxx listen_port=514 python3 sangfor_sip.py
```

## 环境变量说明

| 变量名         | 样例        | 描述         |
|-------------|-----------|------------|
| server_ip   | 127.0.0.1 | 平台IP       |
| server_port | 80        | 平台端口       |
| sk          | sk-xxx    | 连接密钥       |
| listen_port | 514       | 监听Syslog端口 |