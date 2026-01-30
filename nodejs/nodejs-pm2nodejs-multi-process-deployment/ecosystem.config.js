/**
 * PM2 配置文件 - 定义多进程部署策略
 * 使用命令: pm2 start ecosystem.config.js
 */

module.exports = {
  apps: [
    {
      name: 'api-cluster',
      script: './cluster-app.js',
      // 启动实例数量，'max' 表示使用CPU核心数
      instances: 'max',
      // 执行模式：'fork'（单进程）或 'cluster'（多进程集群）
      exec_mode: 'cluster',
      // 自动重启：文件变化时重新加载
      watch: true,
      // 监控目录（可选）
      watch_delay: 1000,
      ignore_watch: ['node_modules', 'logs'],
      // 环境变量
      env: {
        NODE_ENV: 'development',
        PORT: 3000
      },
      env_production: {
        NODE_ENV: 'production',
        PORT: 3000,
        LOG_LEVEL: 'info'
      },
      // 日志配置
      log_type: 'json',
      log_file: 'logs/pm2-app.log',
      out_file: 'logs/out.log',
      error_file: 'logs/error.log',
      // 最大内存限制，超出则重启
      max_memory_restart: '200M',
      // 启动延迟
      wait_ready: true,
      listen_timeout: 5000,
      kill_timeout: 5000,
      // 实例 ID 注入
      instance_var: 'INSTANCE_ID'
    }
  ],

  // 部署配置（可选）
  deploy: {
    production: {
      user: 'node',
      host: 'your-server.com',
      ref: 'origin/main',
      repo: 'git@github.com:username/repo.git',
      path: '/var/www/production',
      'post-deploy': 'npm install && pm2 reload ecosystem.config.js --env production'
    }
  }
};