# RouterOS

RouterOS封禁模块

## 下载模块

```shell
wget https://raw.githubusercontent.com/SecAegis/SecAutoBan/main/device/block/router_os/router_os.py
```

## 安装依赖

```shell
pip3 install SecAutoBan RouterOS-api
```

## 配置RouterOS

### 开启API

登录RouterOS管理后台，开启`IP`-`Services`-`api`

![](./img/1.jpg)

### 创建Address Lists

导航至：`IP`-`Firewall`-`Address Lists`。添加一条Address，其中Name为`sec_auto_ban`，IP填写一个不存在的即可。

![](./img/2.jpg)

### 创建防火墙规则

导航至：`IP`-`Firewall`-`Filter Rules`添加两条规则，分别丢弃来源和目的IP是Address Lists中的IP。

丢弃来源IP：

![](./img/3.jpg)

![](./img/4.jpg)

丢弃目的IP：

![](./img/5.jpg)

![](./img/4.jpg)

## 运行

```shell
server_ip=127.0.0.1 server_port=80 sk=sk-xxx ros_host=10.0.0.1 ros_port=8728 ros_username=admin ros_password=xxx ros_plaintext_login=true ros_list_name=sec_auto_ban python3 router_os.py
```

## 环境变量说明

| 变量名                 | 样例           | 描述                               |
|---------------------|--------------|----------------------------------|
| server_ip           | 127.0.0.1    | 平台IP                             |
| server_port         | 80           | 平台端口                             |
| sk                  | sk-xxx       | 连接密钥                             |
| ros_host            | 10.0.0.1     | 与RouterOS连接的IP                   |
| ros_port            | 8728         | 默认端口8728，如自定义请修改                 |
| ros_username        | admin        | RouterOS用户名                      |
| ros_password        | xxx          | RouterOS密码                       |
| ros_plaintext_login | true         | 适用于 RouterOS 6.43 及更高版本          |
| ros_list_name       | sec_auto_ban | 与Address Lists name保持一致，正常情况无需修改 |
