# 微步蜜罐HFish

## 下载模块

```
wget https://raw.githubusercontent.com/SecAegis/SecAutoBan/main/device/alarm/threatbook_hfish/threatbook_hfish.py
```

## 安装依赖

```
pip3 install SecAutoBan requests
```

## 配置hfish

#### 配置`api_key`

进入`平台管理-系统配置-API配置`页面，复制api_key

![](./img/1.jpg)


## 运行

```shell
server_ip=127.0.0.1 server_port=80 sk=sk-xxx hfish_url=https://xxx.xxx.xxx.xxx:4433 hfish_api_key=xxx hfish_refresh_time=30 python3 threatbook_hfish.py
```

## 环境变量说明

| 变量名                | 样例                           | 描述            |
|--------------------|------------------------------|---------------|
| server_ip          | 127.0.0.1                    | 平台IP          |
| server_port        | 80                           | 平台端口          |
| sk                 | sk-xxx                       | 连接密钥          |
| hfish_url          | https://xxx.xxx.xxx.xxx:4433 | hfish url     |
| hfish_api_key      | xxx                          | hfish api key |
| hfish_refresh_time | 30                           | hfish 轮询时间(秒) |

