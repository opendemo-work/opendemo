/**
 * watch-config.js
 * 功能：监听Consul中KV存储的配置变化，实现动态配置热更新
 */

const Consul = require('consul');
const consul = new Consul();

// 配置键路径
const configKey = 'config/demo-service';

// 创建一个watch实例，用于监听KV变更
const watcher = consul.watch({
  method: consul.kv.get,
  options: { key: configKey }
});

// 解析配置值（假设为JSON）
function parseValue(buf) {
  if (!buf || !buf.Value) return null;
  const str = Buffer.from(buf.Value, 'base64').toString();
  try {
    return JSON.parse(str);
  } catch (e) {
    console.warn('⚠️ 无法解析JSON配置:', str);
    return str;
  }
}

// 首次获取配置
consul.kv.get({ key: configKey }, (err, result) => {
  if (err) {
    console.error('❌ 初始配置读取失败:', err.message);
    return;
  }

  const config = parseValue(result);
  console.log('📝 初始配置加载：', config);
});

// 开始监听配置变化
watcher.on('change', (data, res) => {
  const newConfig = parseValue(data);
  console.log('🔄 配置已更新：', newConfig);
});

watcher.on('error', (err) => {
  console.error('❌ 配置监听出错:', err.message);
});

console.log('⏳ 正在监听配置变化... 修改KV可触发更新');