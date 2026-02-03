// basic-interpolation.js
// 基础模板字符串示例：变量插值

// 定义用户信息变量
const name = '张三';
const age = 25;

// 使用模板字符串插入变量，替代传统拼接方式
// 反引号允许直接嵌入变量，语法为 ${变量名}
const message = `你好，${name}！你今年${age}岁。`;

// 输出结果
console.log(message);

// 对比传统字符串拼接（不推荐）
// const oldMessage = '你好，' + name + '！你今年' + age + '岁。';
// 模板字符串更清晰、易维护