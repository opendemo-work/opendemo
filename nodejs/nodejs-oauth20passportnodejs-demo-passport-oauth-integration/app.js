/**
 * OAuth2.0 + Passport.js 示例主文件
 * 使用Google OAuth20策略实现第三方登录
 */

// 加载环境变量
require('dotenv').config();

// 引入核心模块
const express = require('express');
const passport = require('passport');
const session = require('express-session');
const GoogleStrategy = require('passport-google-oauth20').Strategy;

// 初始化Express应用
const app = express();

// 配置session中间件（生产环境应使用Redis等持久化存储）
app.use(session({
  secret: process.env.SESSION_SECRET || 'dev_secret_key',
  resave: false,
  saveUninitialized: true
}));

// 初始化Passport并绑定session
app.use(passport.initialize());
app.use(passport.session());

// 配置Google OAuth20策略
passport.use(new GoogleStrategy({
  clientID: process.env.GOOGLE_CLIENT_ID,
  clientSecret: process.env.GOOGLE_CLIENT_SECRET,
  callbackURL: "/auth/google/callback"
}, (accessToken, refreshToken, profile, done) => {
  // 在此处可将用户保存到数据库
  console.log('👤 用户信息：', {
    id: profile.id,
    displayName: profile.displayName,
    email: profile.emails?.[0]?.value,
    photo: profile.photos?.[0]?.value
  });
  return done(null, profile); // 用户对象附加到req.user
}));

// 序列化用户到session
passport.serializeUser((user, done) => {
  done(null, user.id);
});

// 从session反序列化用户
passport.deserializeUser((id, done) => {
  // 实际项目中应根据id查询数据库
  done(null, { id });
});

// === 路由定义 ===

// 根路径欢迎页
app.get('/', (req, res) => {
  if (req.isAuthenticated()) {
    const user = req.user;
    const name = user.displayName || '用户';
    const email = user.emails?.[0]?.value || '未知邮箱';
    res.send(`🎉 欢迎，${name}！<br>📧 邮箱：${email}<br><a href="/logout">登出</a>`);
  } else {
    res.send('👋 欢迎！<br><a href="/auth/google">点击使用Google登录</a>');
  }
});

// 触发Google OAuth认证
app.get('/auth/google', passport.authenticate('google', {
  scope: ['profile', 'email'] // 请求用户基本信息和邮箱
}));

// Google回调处理
app.get('/auth/google/callback',
  passport.authenticate('google', { failureRedirect: '/' }),
  (req, res) => {
    // 成功认证后重定向到主页
    res.redirect('/');
  }
);

// 登出路由
app.get('/logout', (req, res) => {
  req.logout(() => {
    res.redirect('/');
  });
});

// 启动服务器
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`✅ 服务器运行在 http://localhost:${PORT}`);
  console.log(`👉 请访问 http://localhost:${PORT}/auth/google 开始Google登录`);
});