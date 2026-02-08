# 🟩 Node.js 命令行速查表 (nodejs-cli.md)

> Node.js开发必备的命令行参考手册，涵盖npm/yarn、调试、性能分析、部署等核心功能，按功能分类整理，方便快速查找和使用

---

## 📋 目录索引

- [npm/yarn包管理](#npmyarn包管理)
- [Node.js调试](#nodejs调试)
- [性能分析](#性能分析)
- [测试工具](#测试工具)
- [构建工具](#构建工具)
- [部署工具](#部署工具)
- [进程管理](#进程管理)
- [版本管理](#版本管理)
- [最佳实践](#最佳实践)

---

## npm/yarn包管理

### 基础操作
```bash
# 初始化项目
npm init
npm init -y
yarn init -y

# 安装包
npm install express
npm install -D nodemon  # 开发依赖
yarn add lodash
yarn add -D webpack

# 全局安装
npm install -g pm2
yarn global add nodemon

# 卸载包
npm uninstall express
yarn remove lodash
```

### 依赖管理
```bash
# 查看过时包
npm outdated
yarn outdated

# 更新包
npm update
yarn upgrade

# 安全审计
npm audit
npm audit fix
yarn audit

# 查看依赖树
npm ls
npm ls --depth=0
yarn list --depth=0
```

---

## Node.js调试

### 内置调试器
```bash
# 启动调试模式
node --inspect app.js
node --inspect-brk app.js  # 在第一行断点

# Chrome DevTools调试
# 访问 chrome://inspect
# 或者使用 VS Code 调试配置

# 调试脚本
node inspect app.js
```

### VS Code调试配置
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "type": "node",
            "request": "launch",
            "name": "Launch Program",
            "program": "${workspaceFolder}/app.js",
            "env": {
                "NODE_ENV": "development"
            }
        }
    ]
}
```

---

## 性能分析

### 内置性能工具
```bash
# CPU性能分析
node --prof app.js
node --prof-process isolate-*.log > processed.txt

# 内存快照
node --inspect app.js
# 然后在Chrome DevTools中使用Memory面板

# 堆快照
node --inspect app.js
# Memory -> Take heap snapshot
```

### 第三方分析工具
```bash
# Clinic.js工具套件
npm install -g clinic
clinic doctor -- node app.js
clinic flame -- node app.js
clinic bubbleprof -- node app.js

# 0x火焰图
npm install -g 0x
0x app.js
```

---

## 测试工具

### Jest测试框架
```bash
# 安装Jest
npm install -D jest
yarn add -D jest

# 运行测试
npm test
yarn test

# 覆盖率报告
jest --coverage
npm test -- --coverage

# 监听模式
jest --watch
```

### Mocha测试框架
```bash
# 安装Mocha
npm install -D mocha chai
yarn add -D mocha chai

# 运行测试
mocha test/**/*.js
npx mocha test/**/*.js

# 测试报告
mocha --reporter spec
mocha --reporter html > report.html
```

---

## 构建工具

### Webpack
```bash
# 安装Webpack
npm install -D webpack webpack-cli
yarn add -D webpack webpack-cli

# 基础构建
npx webpack
webpack --config webpack.config.js

# 开发模式
webpack --mode development
webpack serve
```

### Rollup
```bash
# 安装Rollup
npm install -D rollup
yarn add -D rollup

# 基础打包
rollup -c
rollup src/main.js --file dist/bundle.js --format cjs
```

---

## 部署工具

### PM2进程管理
```bash
# 安装PM2
npm install -g pm2

# 启动应用
pm2 start app.js
pm2 start ecosystem.config.js

# 管理进程
pm2 list
pm2 stop app
pm2 restart app
pm2 delete app

# 监控
pm2 monit
pm2 logs
```

### Docker部署
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 3000
CMD ["node", "server.js"]
```

```bash
docker build -t myapp .
docker run -p 3000:3000 myapp
```

---

## 进程管理

### Forever
```bash
# 安装Forever
npm install -g forever

# 启动守护进程
forever start app.js
forever start -c "node --harmony" app.js

# 管理进程
forever list
forever stop app.js
forever restart app.js
```

### Nodemon开发工具
```bash
# 安装Nodemon
npm install -g nodemon

# 自动重启
nodemon app.js
nodemon --exec python app.py

# 配置文件 nodemon.json
{
    "watch": ["src"],
    "ext": "js,json",
    "ignore": ["src/**/*.test.js"],
    "exec": "node src/index.js"
}
```

---

## 版本管理

### NVM Node版本管理
```bash
# 安装NVM
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# 管理Node版本
nvm install 18
nvm use 18
nvm alias default 18
nvm ls
```

### 项目版本配置
```json
// package.json
{
    "engines": {
        "node": ">=16.0.0",
        "npm": ">=8.0.0"
    }
}
```

---

## 最佳实践

### 环境变量管理
```bash
# 安装dotenv
npm install dotenv

# .env文件
NODE_ENV=production
DATABASE_URL=mongodb://localhost:27017/myapp
PORT=3000

// app.js
require('dotenv').config()
const port = process.env.PORT || 3000
```

### 脚本配置
```json
// package.json
{
    "scripts": {
        "start": "node server.js",
        "dev": "nodemon server.js",
        "test": "jest",
        "build": "webpack --mode production",
        "lint": "eslint src/",
        "prettier": "prettier --write src/"
    }
}
```

### 性能监控脚本
```javascript
// monitor.js
const os = require('os');
const v8 = require('v8');

setInterval(() => {
    const usage = process.memoryUsage();
    console.log({
        rss: Math.round(usage.rss / 1024 / 1024) + 'MB',
        heapTotal: Math.round(usage.heapTotal / 1024 / 1024) + 'MB',
        heapUsed: Math.round(usage.heapUsed / 1024 / 1024) + 'MB',
        external: Math.round(usage.external / 1024 / 1024) + 'MB'
    });
}, 5000);
```

---