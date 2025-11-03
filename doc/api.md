# SecAutoBan API 使用说明

> API 样例脚本：[api_example](./api_example.py)

## 概述
SecAutoBan 提供对“封禁（黑名单）”与“白名单”资源的增删改查接口。所有请求体（request body）与响应体（response body）都是使用 AES-GCM 对称加密后的二进制数据，脚本内用 sk 做本地加解密，HTTP 头部携带 ak 作为访问标识。

## 配置项（api_example.py 中）

- base_url: 后端地址（例如 `http://127.0.0.1:8080`）
- ak: 访问 Key（需要在 headers 中发送）
- sk: 对称加密密钥（用于 AES-GCM，本地加解密，不直接放到网络请求中）

示例请求头：

```
{
  "ak": ak
}
```

## 加解密说明
- 算法：AES-GCM
- 加密函数返回布局：nonce(12 bytes) || ciphertext || tag(16 bytes)
- 解密时以 data[:12] 作为 nonce，data[-16:] 作为 tag，data[12:-16] 为 ciphertext

样例脚本中对应函数：
- encrypt_aes_gcm(data: bytes, sk: str) -> bytes
- decrypt_aes_gcm(data: bytes, sk: str) -> bytes

请求流程（客户端）：
1. 将 JSON 请求体 bytes 化（utf-8 编码）。
2. 使用 encrypt_aes_gcm 加密得到二进制 payload。
3. 以 HTTP 方法请求相应端点，body 使用加密后的二进制，headers 中包含 ak。
4. 服务器返回加密二进制响应，客户端用 decrypt_aes_gcm 解密并解析 JSON。

## 通用约定
- 所有请求的 body 都应为 encrypt_aes_gcm 的输出（nonce+ciphertext+tag）。
- 所有响应为相同格式的加密数据，需要 decrypt_aes_gcm 后再解析。
- 响应常见成功格式（示例）：{"status": "success", ...}
- 当响应长度小于 28 字节（nonce 12 + tag 16）视为无有效返回。

## API 列表与字段（详细）

### /api/ban - 黑名单（封禁 IP / Cidr）
1. 查询（POST）
   - HTTP 方法：POST
   - 请求体 JSON：
     {
       "ipCidr": string,   // 支持 IP 或 CIDR 表达式，空串或 "0.0.0.0/0" 可用于通配
       "page": int,        // 页码，从 1 开始
       "size": int         // 每页大小
     }
   - 响应：解密后的 JSON 字符串（通常包含 items、page、size、total 等分页信息）

2. 添加（PUT）
   - HTTP 方法：PUT
   - 请求体 JSON：
     {
       "ipCidr": string,
       "expiresTime": int,     // -1: 平台自动计算过期 | 0: 永不过期 | 毫秒级时间戳
       "attackAsset": string,  // 攻击资产描述
       "attackMethod": string, // 攻击方式
       "remark": string
     }
   - 响应：解密后 JSON，若 status == "success" 则表示成功
   - 返回（脚本 wrapper）：布尔 True/False

3. 更新（PATCH）
   - HTTP 方法：PATCH
   - 请求体 JSON：与添加类似，额外：
     {
       "status": bool   // true 表示启用该封禁，false 表示禁用
     }
   - 响应：同上，脚本返回布尔

4. 删除（DELETE）
   - HTTP 方法：DELETE
   - 请求体 JSON：
     {
       "ipCidr": string
     }
   - 响应：解密后 JSON，status == "success" 为成功，脚本返回布尔

### /api/whitelist - 白名单（加白 IP / Cidr）
1. 查询（POST）
   - HTTP 方法：POST
   - 请求体 JSON：
     {
       "ipCidr": string,
       "page": int,
       "size": int
     }
   - 响应：解密后的 JSON 字符串（分页/列表）

2. 添加（PUT）
   - HTTP 方法：PUT
   - 请求体 JSON：
     {
       "ipCidr": string,
       "expiresTime": int, // 0: 永不过期 | 毫秒级时间戳
       "class": string,    // 白名单类别
       "remark": string
     }
   - 响应：status == "success" 表示成功，脚本返回布尔

3. 更新（PATCH）
   - HTTP 方法：PATCH
   - 请求体 JSON：同添加，额外包含
     {
       "status": bool
     }
   - 响应：同上，脚本返回布尔

4. 删除（DELETE）
   - HTTP 方法：DELETE
   - 请求体 JSON：
     {
       "ipCidr": string
     }
   - 响应：同上，脚本返回布尔

## 使用示例（Python，基于 api_example.py 中封装函数）
- 先在脚本中设置 base_url / ak / sk，然后直接调用封装函数，例如：
  - get_ban_ip_cidr("0.0.0.0/0", page=1, size=100)
  - add_ban_ip_cidr("3.3.3.3", -1, "资产", "攻击方式", "备注")
  - add_white_ip_cidr("8.8.8.8/8", int((time.time()+86400)*1000), "类别", "备注")

注意：直接用 curl 等工具调用需要自行实现同样的 AES-GCM 加密/解密流程；不可直接发送明文 JSON 到这些端点。

## 错误处理建议
- 检查响应最小长度（>= 28 bytes），不足则视为网络或服务异常。
- 解密失败（AES verify 错误）应记录并报警，可能表示 sk 或返回数据被篡改。
- 后端返回非 success 状态时，应读取返回的错误字段（如果有）并根据业务决策重试或上报。

## 安全与运维建议
- sk 必须妥善保管，仅用于本地进程内加解密，避免写入版本控制或日志。
- ak 作为访问凭证应按最小权限原则分发，定期轮换。
- 建议在 TLS（HTTPS）上部署接口，尽管请求体本身加密，TLS 仍然能保护报头与传输元数据。
- 校验 sk 长度并在脚本启动时报错（脚本示例中没有严格校验，部署前补充校验）。

## 开发者注
- api_example.py 提供了对上述接口的调用封装，建议在生产使用前补充：
  - 密钥长度校验与错误处理
  - 超时与重试策略（requests timeout）
  - 日志与审计

