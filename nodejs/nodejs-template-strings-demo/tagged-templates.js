// tagged-templates.js
// 标签模板（Tagged Templates）基础示例

// 定义一个标签函数，用于处理模板字符串
// 第一个参数是字符串片段数组，后续是插值表达式的值
function log(level, time, message) {
  return `日志级别: ${level} - 时间: ${time.toISOString()} - 消息: ${message}`;
}

// 使用标签函数调用模板字符串
// 注意：log 后紧跟反引号，不是括号
const level = 'INFO';
const timestamp = new Date(); // 当前时间
const msg = '用户登录成功';

const logEntry = log`\${level} \${timestamp} \${msg}`;

// 实际上，上面的写法有误，正确应为：
// 我们重新定义一个正确的标签函数示例

function simpleTag(strings, ...values) {
  let result = '';
  strings.forEach((str, i) => {
    result += str;
    if (i < values.length) {
      result += values[i];
    }
  });
  return `处理后的日志: ${result.trim()}`;
}

// 正确使用标签模板
const user = 'Alice';
const action = '登录';
const entry = simpleTag`用户 ${user} 执行了 ${action} 操作`;

console.log(entry);