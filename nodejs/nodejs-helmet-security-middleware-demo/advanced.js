/**
 * 高级安全配置示例
 * 自定义Helmet策略以满足特定安全需求
 */

const express = require('express');
const helmet = require('helmet');

const app = express();

// 自定义Helmet配置：精细化控制安全头
app.use(
  helmet({
    // 内容安全策略：仅允许同源资源
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        scriptSrc: ["'self'", "'unsafe-inline'"],
        styleSrc: ["'self'", "'unsafe-inline'"],
        imgSrc: ["'self'", "data:"],
        connectSrc: ["'self'"],
        fontSrc: ["'self'"],
        objectSrc: ["'none'"],
        mediaSrc: ["'self'"],
        frameAncestors: ["'none'"]
      }
    },
    // 强制HTTPS，有效期1年
    hsts: {
      maxAge: 31536000, // 1年（秒）
      includeSubDomains: true,
      preload: true
    },
    // 防止点击劫持：禁止在iframe中加载
    frameguard: {
      action: 'deny'
    },
    // 防止MIME嗅探
    noSniff: true,
    // XSS过滤器启用
    xssFilter: true
  })
);

app.get('/', (req, res) => {
  res.send('<h1>🔐 高级安全页面 - 自定义CSP与HSTS已生效</h1>');
});

const PORT = 3001;
app.listen(PORT, () => {
  console.log(`✅ 高级安全服务器运行在 http://localhost:${PORT}`);
});

// 【最佳实践】
// - 生产环境建议启用HSTS和严格CSP
// - 根据前端框架调整script-src策略（如需'unsafe-inline'）