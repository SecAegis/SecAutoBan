# 深信服态势感知


## 下载模块

```
wget https://raw.githubusercontent.com/SecAegis/SecAutoBan/main/device/alarm/sangfor_sip/sangfor_sip.py
```

## 配置说明

### 配置深信服态势感知

添加syslog推送，由于默认数据包过大，UDP存在截断问题，需选择TCP推送。

### 安装依赖

```
pip3 install SecAutoBan
```

### 配置模块

#### 修改回连核心模块配置

更改脚本第`40`-`42`行

```
server_ip = "127.0.0.1",
server_port = 80,
sk = "sk-xxx",
```

#### 配置syslog监听地址

更改脚本第`38`行，请与天眼SYSLOG中配置的端口一致

```
listen_syslog_tcp_port = 567
```

## 运行

```shell
python3 sangfor_sip.py
```