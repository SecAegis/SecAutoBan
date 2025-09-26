# 奇安信天眼

## 下载模块

```shell
wget https://raw.githubusercontent.com/SecAegis/SecAutoBan/main/device/alarm/qianxin_skyeye/qianxin_skyeye.py
```

## 安装依赖

```shell
pip3 install SecAutoBan
```

## 配置说明

### 配置天眼

天眼支持外发syslog，通过`设置`-`联动管理`-`告警联动配置`-`SYSLOG配置`，打开syslog服务开关。

![](./img/1.jpg)

新增一条配置

![](./img/2.jpg)

新增一条配置，服务器IP为本脚本运行的服务器IP，传输方式选择UDP，打开告警日志开关配置告警日志

![](./img/3.jpg)

告警字段选择如下：

![](./img/4.jpg)

配置完成后依次点击保存即可

## 运行

```shell
server_ip=127.0.0.1 server_port=80 sk=sk-xxx listen_port=514 python3 qianxin_skyeye.py
```

## 环境变量说明

| 变量名         | 样例        | 描述         |
|-------------|-----------|------------|
| server_ip   | 127.0.0.1 | 平台IP       |
| server_port | 80        | 平台端口       |
| sk          | sk-xxx    | 连接密钥       |
| listen_port | 514       | 监听Syslog端口 |