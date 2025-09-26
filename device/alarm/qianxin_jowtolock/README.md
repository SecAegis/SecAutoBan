# 奇安信椒图

## 下载模块

```
wget https://raw.githubusercontent.com/SecAegis/SecAutoBan/main/device/alarm/qianxin_jowtolock/qianxin_jowtolock.py
```

## 安装依赖

```
pip3 install SecAutoBan
```

## 配置说明

### 配置天眼

椒图外发syslog需要登录superadmin账号，登录后通过`后台设置`-`日志推送`，添加推送任务。

日志类型选择`网络攻击日志`、`威胁感知事件`

![](./img/1.jpg)

时间类型选择高危：

![](./img/2.jpg)

配置完成点击确定即可。

## 运行

```shell
server_ip=127.0.0.1 server_port=80 sk=sk-xxx listen_port=514 python3 qianxin_jowtolock.py
```

## 环境变量说明

| 变量名         | 样例        | 描述         |
|-------------|-----------|------------|
| server_ip   | 127.0.0.1 | 平台IP       |
| server_port | 80        | 平台端口       |
| sk          | sk-xxx    | 连接密钥       |
| listen_port | 514       | 监听Syslog端口 |