# SSL 证书

请将证书合并为 cert.pem 放在此目录。
生成测试证书：

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout key.pem -out cert.pem -subj '/CN=localhost'
cat cert.pem key.pem > certs/cert.pem
```
