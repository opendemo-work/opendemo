# Node.js CLI命令详解

本文档详细解释Node.js开发常用CLI命令的用途、输出示例、内容解析、注意事项以及在生产环境中执行的安全风险。

## 1. node (Node.js运行时)

### 用途
`node` 是Node.js JavaScript运行时的主命令，用于执行JavaScript文件、启动REPL环境或运行内联代码。

### 输出示例
```bash
# 运行JavaScript文件
$ node app.js
Server running on port 3000
Connected to database successfully

# 启动交互式REPL环境
$ node
Welcome to Node.js v18.12.1.
Type ".help" for more information.
> console.log('Hello World');
Hello World
undefined
> const sum = (a, b) => a + b;
undefined
> sum(5, 3);
8
> .exit

# 执行内联代码
$ node -e "console.log('Current time:', new Date().toISOString())"
Current time: 2023-12-07T19:30:15.123Z

# 查看Node.js版本
$ node --version
v18.12.1

# 查看详细版本信息
$ node --version --v8-options
v18.12.1
SSE3=1 SSSE3=1 SSE4_1=1 SSE4_2=1 SAHF=1 AVX=1 FMA3=1 AVX2=1 BMI1=1 BMI2=1
V8 version 10.2.154.15-node.12

# 启用检查器调试
$ node --inspect app.js
Debugger listening on ws://127.0.0.1:9229/12345678-1234-1234-1234-123456789012
For help, see: https://nodejs.org/en/docs/inspector

# 设置环境变量运行
$ NODE_ENV=production node server.js
Production server started on port 8080

# 限制内存使用
$ node --max-old-space-size=4096 app.js
Application started with 4GB heap limit

# 启用ES模块支持
$ node --experimental-modules app.mjs
(node:12345) ExperimentalWarning: The ESM module loader is experimental.
Hello from ES Module!
```

### 内容解析
- **版本信息**: 显示Node.js和V8引擎版本
- **调试信息**: 显示调试器监听地址和端口
- **环境变量**: 运行时的环境配置
- **内存限制**: 堆内存大小限制信息
- **警告信息**: 实验性功能警告

### 常用参数详解
- `-e, --eval <script>`: 执行字符串脚本
- `-i, --interactive`: 强制进入REPL模式
- `--inspect[=[host:]port]`: 启用调试器
- `--max-old-space-size=<size>`: 设置老生代内存限制(MB)
- `--no-warnings`: 禁用警告信息
- `--trace-warnings`: 显示警告堆栈跟踪
- `--experimental-modules`: 启用ES模块实验性支持

### 注意事项
- 生产环境应固定Node.js版本
- 合理设置内存限制避免OOM
- 启用适当的错误处理机制
- 监控应用性能和资源使用

### 安全风险
- ⚠️ 执行不受信任的JavaScript代码存在风险
- ⚠️ 调试端口暴露可能带来安全威胁
- ⚠️ 环境变量可能包含敏感配置信息
- ⚠️ 内存限制设置不当可能影响稳定性

## 2. npm (Node包管理器)

### 用途
`npm` 是Node.js的默认包管理器，用于安装、发布和管理JavaScript包和依赖。

### 输出示例
```bash
# 初始化新项目
$ npm init
This utility will walk you through creating a package.json file.
It only covers the most common items, and tries to guess sensible defaults.

See `npm help json` for definitive documentation on these fields
and exactly what they do.

Use `npm install <pkg>` afterwards to install a package and
save it as a dependency in the package.json file.

Press ^C at any time to quit.
package name: (my-project) 
version: (1.0.0) 
description: My awesome Node.js project
entry point: (index.js) 
test command: 
git repository: 
keywords: 
author: John Doe
license: (ISC) 
About to write to /home/user/my-project/package.json:

{
  "name": "my-project",
  "version": "1.0.0",
  "description": "My awesome Node.js project",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "author": "John Doe",
  "license": "ISC"
}


Is this OK? (yes) yes

# 安装包
$ npm install express
npm WARN deprecated formidable@1.2.6: Please upgrade to latest, formidable@v2 or formidable@v3!
npm notice Beginning October 26, 2021, all connections to the npm registry - including for package installation - must use TLS 1.2 or higher. You are currently using plaintext http to connect. Please visit the GitHub blog for more information: https://github.blog/2021-08-23-npm-registry-deprecating-tls-1-0-tls-1-1/
npm WARN EBADENGINE Unsupported engine {
npm WARN EBADENGINE   package: 'express@4.18.2',
npm WARN EBADENGINE   required: { node: '>= 0.10.0' },
npm WARN EBADENGINE   current: { node: 'v18.12.1' }
npm WARN EBADENGINE }

added 57 packages, and audited 58 packages in 3s

found 0 vulnerabilities

# 安装开发依赖
$ npm install --save-dev jest
npm notice New patch version of npm available! 8.19.2 -> 8.19.3
npm notice Changelog: <https://github.com/npm/cli/releases/tag/v8.19.3>
npm notice Run `npm install -g npm@8.19.3` to update!
npm WARN deprecated uuid@3.4.0: Please upgrade  to version 7 or higher.  Older versions may use Math.random() in certain circumstances, which is known to be problematic.  See https://v8.dev/blog/math-random for details.

added 293 packages, and audited 351 packages in 8s

30 packages are looking for funding
  run `npm fund` for details

found 0 vulnerabilities

# 全局安装包
$ npm install -g nodemon
npm WARN deprecated uuid@3.4.0: Please upgrade  to version 7 or higher.  Older versions may use Math.random() in certain circumstances, which is known to be problematic.  See https://v8.dev/blog/math-random for details.

changed 139 packages, and audited 140 packages in 5s

found 0 vulnerabilities

# 查看已安装包
$ npm list
my-project@1.0.0 /home/user/my-project
├── express@4.18.2
└── lodash@4.17.21

$ npm list --depth=0
my-project@1.0.0 /home/user/my-project
├── express@4.18.2
├── lodash@4.17.21
└── moment@2.29.4

# 运行脚本
$ npm run test
> my-project@1.0.0 test
> jest

 PASS  __tests__/app.test.js
  ✓ should return hello world (2 ms)

Test Suites: 1 passed, 1 total
Tests:       1 passed, 1 total
Snapshots:   0 total
Time:        1.234 s
Ran all test suites.

# 审计安全漏洞
$ npm audit
# npm audit report

minimist  <1.2.6
Severity: high
Prototype Pollution - https://npmjs.com/advisories/1179
fix available via `npm audit fix`
node_modules/minimist

1 high severity vulnerability

To address all issues, run:
  npm audit fix

# 修复安全漏洞
$ npm audit fix
npm WARN audit Updating minimist to 1.2.6 because there is one vulnerability advisory for the current version.
fixed 1 vulnerability and audited 58 packages in 2s
found 0 vulnerabilities

# 发布包
$ npm publish
npm notice 
npm notice 📦  my-package@1.0.0
npm notice === Tarball Contents === 
npm notice 1.1kB package.json
npm notice 123B  index.js
npm notice 456B  README.md
npm notice === Tarball Details === 
npm notice name:          my-package
npm notice version:       1.0.0
npm notice filename:      my-package-1.0.0.tgz
npm notice package size:  890 bytes
npm notice unpacked size: 1.6 kB
npm notice shasum:        abcdef1234567890abcdef1234567890abcdef12
npm notice integrity:     sha512-AbCdEf1234567[...]AbCdEf1234567==
npm notice total files:   3
npm notice 
npm notice Publishing to https://registry.npmjs.org/
+ my-package@1.0.0
```

### 内容解析
- **依赖树**: 显示包的依赖关系结构
- **安全警告**: 显示已知的安全漏洞
- **版本信息**: 显示包的版本和兼容性
- **审计报告**: 安全漏洞的详细分析
- **发布信息**: 包发布的详细过程

### 常用参数详解
- `init`: 初始化package.json
- `install <package>`: 安装包
- `install --save-dev <package>`: 安装开发依赖
- `install -g <package>`: 全局安装
- `list`: 查看已安装包
- `run <script>`: 运行package.json中的脚本
- `audit`: 审计安全漏洞
- `audit fix`: 自动修复漏洞
- `publish`: 发布包到npm仓库

### 注意事项
- 定期更新依赖修复安全漏洞
- 使用package-lock.json锁定版本
- 生产环境应审核第三方包
- 注意包的许可证兼容性

### 安全风险
- ⚠️ 第三方包可能存在安全漏洞
- ⚠️ 恶意包可能窃取敏感信息
- ⚠️ 过时的依赖包存在已知漏洞
- ⚠️ 依赖包的依赖链可能引入风险

## 3. yarn (快速包管理器)

### 用途
`yarn` 是Facebook开发的快速、可靠、安全的JavaScript包管理器，作为npm的替代方案。

### 输出示例
```bash
# 初始化项目
$ yarn init
yarn init v1.22.19
question name (my-project): 
question version (1.0.0): 
question description: My awesome project
question entry point (index.js): 
question repository url: 
question author: John Doe
question license (MIT): 
success Saved package.json
✨  Done in 23.45s.

# 安装依赖
$ yarn add express lodash
yarn add v1.22.19
info No lockfile found.
[1/4] 🔍  Resolving packages...
[2/4] 🚚  Fetching packages...
[3/4] 🔗  Linking dependencies...
[4/4] 🔨  Building fresh packages...
success Saved lockfile.
success Saved 57 new dependencies.
info Direct dependencies
├─ express@4.18.2
└─ lodash@4.17.21
info All dependencies
├─ accepts@1.3.8
├─ array-flatten@1.1.1
├─ body-parser@1.20.1
# ... 更多依赖 ...
✨  Done in 5.67s.

# 安装开发依赖
$ yarn add --dev jest supertest
yarn add v1.22.19
[1/4] 🔍  Resolving packages...
[2/4] 🚚  Fetching packages...
[3/4] 🔗  Linking dependencies...
[4/4] 🔨  Building fresh packages...
success Saved 293 new dependencies.
info Direct dependencies
├─ jest@29.3.1
└─ supertest@6.3.1
✨  Done in 8.91s.

# 安装所有依赖
$ yarn install
yarn install v1.22.19
[1/4] 🔍  Resolving packages...
[2/4] 🚚  Fetching packages...
[3/4] 🔗  Linking dependencies...
[4/4] 🔨  Building fresh packages...
success Saved lockfile.
✨  Done in 12.34s.

# 运行脚本
$ yarn test
yarn run v1.22.19
$ jest
 PASS  __tests__/app.test.js
  ✓ GET / should return hello world (15 ms)

Test Suites: 1 passed, 1 total
Tests:       1 passed, 1 total
Snapshots:   0 total
Time:        1.234 s, estimated 2 s
Ran all test suites.
✨  Done in 2.34s.

# 查看依赖信息
$ yarn list
yarn list v1.22.19
├─ accepts@1.3.8
├─ array-flatten@1.1.1
├─ body-parser@1.20.1
├─ express@4.18.2
└─ lodash@4.17.21

# 升级依赖
$ yarn upgrade express
yarn upgrade v1.22.19
[1/4] 🔍  Resolving packages...
[2/4] 🚚  Fetching packages...
[3/4] 🔗  Linking dependencies...
[4/4] 🔨  Rebuilding all packages...
success Saved lockfile.
success Saved 1 new dependency.
info Direct dependencies
└─ express@4.18.2
✨  Done in 3.45s.

# 移除依赖
$ yarn remove lodash
yarn remove v1.22.19
[1/2] 🗑  Removing module lodash...
[2/2] 🔨  Regenerating lockfile and installing missing dependencies...
success Uninstalled packages.
✨  Done in 2.34s.

# 检查过时依赖
$ yarn outdated
yarn outdated v1.22.19
info Color legend : 
 "<red>"    : Major Update backward-incompatible updates 
 "<yellow>" : Minor Update backward-compatible features 
 "<green>"  : Patch Update backward-compatible bug fixes
Package    Current Wanted Latest Package Type    URL
express    4.17.1  4.18.2 4.18.2 dependencies    https://expressjs.com/
lodash     4.17.20 4.17.21 4.17.21 dependencies    https://lodash.com/
```

### 内容解析
- **安装过程**: 显示解析、获取、链接、构建四个阶段
- **依赖信息**: 区分直接依赖和间接依赖
- **版本状态**: 显示当前、期望和最新版本
- **颜色标识**: 用颜色区分更新类型（重大/次要/补丁）

### 常用参数详解
- `init`: 初始化项目
- `add <package>`: 添加依赖
- `add --dev <package>`: 添加开发依赖
- `install`: 安装所有依赖
- `run <script>`: 运行脚本
- `list`: 查看依赖树
- `upgrade <package>`: 升级包
- `remove <package>`: 移除包
- `outdated`: 检查过时依赖

### 注意事项
- yarn.lock文件确保依赖一致性
- 并行安装提高速度
- 离线模式支持缓存使用
- 工作区支持monorepo管理

### 安全风险
- ⚠️ 第三方包可能存在安全问题
- ⚠️ lock文件可能包含恶意包版本
- ⚠️ 并行安装可能引入竞争条件
- ⚠️ 缓存污染可能影响包完整性

## 4. pm2 (进程管理器)

### 用途
`pm2` 是Node.js应用的生产级进程管理器，提供负载均衡、监控、日志管理等功能。

### 输出示例
```bash
# 启动应用
$ pm2 start app.js
[PM2] Starting /home/user/app.js in fork_mode (1 instance)
[PM2] Done.
┌────┬──────────┬─────────────┬────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name     │ namespace   │ version│ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼──────────┼─────────────┼────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ 0  │ app      │ default     │ N/A    │ fork    │ 12345    │ 0s     │ 0    │ online    │ 0%       │ 25.4mb   │ user     │ disabled │
└────┴──────────┴─────────────┴────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘

# 启动多个实例
$ pm2 start server.js -i max
[PM2] Spawning PM2 daemon with pm2_home=/home/user/.pm2
[PM2] PM2 Successfully daemonized
[PM2] Starting /home/user/server.js in cluster_mode (0 instance)
[PM2] App [server] launched (8 instances)
┌────┬──────────┬─────────────┬────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name     │ namespace   │ version│ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼──────────┼─────────────┼────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ 0  │ server   │ default     │ N/A    │ cluster │ 12346    │ 0s     │ 0    │ online    │ 0%       │ 26.1mb   │ user     │ disabled │
│ 1  │ server   │ default     │ N/A    │ cluster │ 12347    │ 0s     │ 0    │ online    │ 0%       │ 25.8mb   │ user     │ disabled │
│ 2  │ server   │ default     │ N/A    │ cluster │ 12348    │ 0s     │ 0    │ online    │ 0%       │ 26.3mb   │ user     │ disabled │
# ... 更多实例 ...

# 查看应用状态
$ pm2 list
┌────┬──────────┬─────────────┬────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name     │ namespace   │ version│ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼──────────┼─────────────┼────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ 0  │ app      │ default     │ 1.0.0  │ fork    │ 12345    │ 2h     │ 0    │ online    │ 1.2%     │ 45.2mb   │ user     │ disabled │
│ 1  │ api      │ default     │ 2.1.0  │ cluster │ 12346    │ 1h     │ 1    │ online    │ 0.8%     │ 67.8mb   │ user     │ disabled │
└────┴──────────┴─────────────┴────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘

# 查看详细信息
$ pm2 show app
 Describing process with id 0 - name app
┌───────────────────┬─────────────────────────────────────────────────┐
│ status            │ online                                          │
│ name              │ app                                             │
│ version           │ 1.0.0                                           │
│ restarts          │ 0                                               │
│ uptime            │ 2h                                              │
│ script path       │ /home/user/app.js                               │
│ script args       │ N/A                                             │
│ error log path    │ /home/user/.pm2/logs/app-error.log              │
│ out log path      │ /home/user/.pm2/logs/app-out.log                │
│ pid path          │ /home/user/.pm2/pids/app-0.pid                  │
│ interpreter       │ node                                            │
│ interpreter args  │ N/A                                             │
│ script id         │ 0                                               │
│ exec cwd          │ /home/user                                      │
│ exec mode         │ fork_mode                                       │
│ node.js version   │ 18.12.1                                         │
│ node env          │ N/A                                             │
│ watch & reload    │ ✘                                               │
│ unstable restarts │ 0                                               │
│ created at        │ 2023-12-07T17:30:15                             │
└───────────────────┴─────────────────────────────────────────────────┘
 Code metrics value
┌─────────────────┬────────┐
│ Loop delay      │ 2.12ms │
│ Active handles  │ 5      │
│ Active requests │ 2      │
└─────────────────┴────────┘

# 查看日志
$ pm2 logs app
[TAILING] Tailing last 15 lines for [app] process (change the value with --lines option)
/home/user/.pm2/logs/app-out.log last 15 lines:
0|app  | 2023-12-07T19:30:15: Server listening on port 3000
0|app  | 2023-12-07T19:30:20: GET /api/users - 200 15ms
0|app  | 2023-12-07T19:30:25: POST /api/login - 200 45ms

/home/user/.pm2/logs/app-error.log last 15 lines:
0|app  | 2023-12-07T19:25:30: Warning: Deprecated API endpoint called

# 重启应用
$ pm2 restart app
[PM2] Applying action restartProcessId on app [app](ids: 0)
[PM2] [app](0) ✓
┌────┬──────────┬─────────────┬────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name     │ namespace   │ version│ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼──────────┼─────────────┼────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ 0  │ app      │ default     │ 1.0.0  │ fork    │ 12349    │ 0s     │ 1    │ online    │ 0%       │ 25.1mb   │ user     │ disabled │
└────┴──────────┴─────────────┴────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘

# 停止应用
$ pm2 stop app
[PM2] Applying action stopProcessId on app [app](ids: 0)
[PM2] [app](0) ✓
┌────┬──────────┬─────────────┬────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name     │ namespace   │ version│ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼──────────┼─────────────┼────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ 0  │ app      │ default     │ 1.0.0  │ fork    │ 0        │ 0      │ 1    │ stopped   │ 0%       │ 0b       │ user     │ disabled │
└────┴──────────┴─────────────┴────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘

# 删除应用
$ pm2 delete app
[PM2] Applying action deleteProcessId on app [app](ids: 0)
[PM2] [app](0) ✓
```

### 内容解析
- **进程状态**: 显示应用的运行状态和资源使用
- **日志信息**: 区分标准输出和错误输出日志
- **性能指标**: 显示CPU、内存、循环延迟等指标
- **重启计数**: 显示应用重启次数

### 常用参数详解
- `start <app>`: 启动应用
- `start <app> -i <instances>`: 启动多个实例
- `list`: 查看所有应用状态
- `show <app>`: 查看应用详细信息
- `logs <app>`: 查看应用日志
- `restart <app>`: 重启应用
- `stop <app>`: 停止应用
- `delete <app>`: 删除应用

### 注意事项
- 生产环境建议使用集群模式
- 合理配置日志轮转避免磁盘占满
- 监控应用健康状态和性能指标
- 定期备份PM2配置

### 安全风险
- ⚠️ PM2配置可能包含敏感信息
- ⚠️ 日志文件可能暴露应用内部信息
- ⚠️ 未授权的进程管理操作存在风险
- ⚠️ 网络暴露的监控接口需要保护

## 5. npx (包执行器)

### 用途
`npx` 用于执行npm包中的命令行工具，无需全局安装即可运行。

### 输出示例
```bash
# 运行一次性命令
$ npx create-react-app my-app
Need to install the following packages:
  create-react-app@5.1.0
Ok to proceed? (y) y
Creating a new React app in /home/user/my-app.

Installing packages. This might take a couple of minutes.
Installing react, react-dom, and react-scripts with cra-template...

added 1437 packages in 2m 34s

Success! Created my-app at /home/user/my-app
Inside that directory, you can run several commands:

  npm start
    Starts the development server.

  npm run build
    Bundles the app into static files for production.

  npm test
    Starts the test runner.

  npm run eject
    Removes this tool and copies build dependencies, configuration files
    and scripts into the app directory. If you do this, you can't go back!

We suggest that you begin by typing:

  cd my-app
  npm start

Happy hacking!

# 运行特定版本的包
$ npx node@16 --version
v16.18.1

# 运行本地安装的包
$ npx jest --version
jest@29.3.1

# 从GitHub运行包
$ npx github:expressjs/generator express-app
npx: installed 10 in 2.345s
   create : express-app
   create : express-app/package.json
   create : express-app/app.js
# ... 更多文件 ...

# 执行远程脚本
$ npx https://gist.githubusercontent.com/user/script.js
Running remote script...
Script executed successfully!

# 交互式包选择
$ npx cowsay "Hello World!"
 ______________
< Hello World! >
 --------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```

### 内容解析
- **安装过程**: 显示临时安装包的过程
- **版本选择**: 可以指定特定版本运行
- **执行结果**: 显示命令的执行输出
- **交互提示**: 需要用户确认的操作

### 常用参数详解
- `<command>`: 执行npm包中的命令
- `<package>@<version>`: 指定包版本
- `--package <package>`: 显式指定包名
- `--no-install`: 不安装缺失的包
- `--ignore-existing`: 忽略已安装的包

### 注意事项
- 临时安装的包不会污染全局环境
- 网络不稳定时可能安装失败
- 注意执行不受信任包的安全风险
- 可以结合使用--package参数

### 安全风险
- ⚠️ 执行未知来源的包存在安全风险
- ⚠️ 远程脚本可能包含恶意代码
- ⚠️ 临时安装的包可能有安全漏洞
- ⚠️ 网络传输可能被中间人攻击

## 6. nodemon (开发工具)

### 用途
`nodemon` 是开发时的文件监视工具，当文件发生变化时自动重启Node.js应用。

### 输出示例
```bash
# 基本使用
$ nodemon app.js
[nodemon] 2.0.20
[nodemon] to restart at any time, enter `rs`
[nodemon] watching path(s): *.*
[nodemon] watching extensions: js,mjs,json
[nodemon] starting `node app.js`
Server running on port 3000
[nodemon] clean exit - waiting for changes before restart

# 修改文件后自动重启
# [nodemon] restarting due to changes...
# [nodemon] starting `node app.js`
# Server running on port 3000

# 指定监视的文件类型
$ nodemon --ext js,json,html app.js
[nodemon] 2.0.20
[nodemon] watching extensions: js,json,html

# 忽略特定文件
$ nodemon --ignore tests/ --ignore logs/ app.js
[nodemon] 2.0.20
[nodemon] ignoring: /home/user/project/tests/**/* /home/user/project/logs/**/*

# 指定配置文件
$ nodemon --config nodemon.json app.js
[nodemon] 2.0.20
[nodemon] reading config /home/user/project/nodemon.json

# 延迟重启
$ nodemon --delay 2 app.js
[nodemon] 2.0.20
[nodemon] delaying restart for 2 seconds

# 执行其他命令
$ nodemon --exec python server.py
[nodemon] 2.0.20
[nodemon] starting `python server.py`
Python server started on port 8000

# 查看帮助信息
$ nodemon --help
  Usage: nodemon [nodemon options] [script.js] [args]

  See "nodemon --help" for more.
```

### 内容解析
- **监视状态**: 显示正在监视的路径和文件类型
- **重启信息**: 显示重启原因和过程
- **配置信息**: 显示使用的配置选项
- **执行命令**: 显示实际执行的命令

### 常用参数详解
- `<script>`: 要监视的脚本文件
- `--ext <extensions>`: 指定监视的文件扩展名
- `--ignore <patterns>`: 忽略特定文件或目录
- `--delay <seconds>`: 重启延迟时间
- `--exec <command>`: 执行其他命令
- `--config <file>`: 指定配置文件

### 注意事项
- 只在开发环境使用，不要用于生产
- 合理配置忽略规则避免频繁重启
- 注意大项目可能影响性能
- 可以配合调试工具使用

### 安全风险
- ⚠️ 文件监视可能暴露项目结构
- ⚠️ 自动执行可能带来意外风险
- ⚠️ 配置文件可能包含敏感信息
- ⚠️ 网络文件系统可能影响监视效果

---

**总结**: 以上是Node.js开发常用的CLI工具详解。在生产环境中使用这些工具时，务必注意安全配置、依赖管理和性能监控，确保Node.js应用的稳定运行。