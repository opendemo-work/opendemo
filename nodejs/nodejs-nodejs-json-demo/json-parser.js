// =========================================
// 文件名: json-parser.js
// 功能: 演示JSON字符串的解析与序列化
// 作者: Node.js导师
// 最佳实践: 使用try-catch处理解析异常
// =========================================

// 示例1：合法JSON字符串解析
const jsonString = '{"name": "Alice", "age": 30, "city": "Beijing"}';

try {
  // 使用JSON.parse将字符串转换为JS对象
  const parsedData = JSON.parse(jsonString);
  console.log('✅ 解析成功：', parsedData);

  // 使用JSON.stringify将对象转回字符串
  const serialized = JSON.stringify(parsedData);
  console.log('🔄 序列化回字符串：', serialized);
} catch (error) {
  // 捕获JSON格式错误
  console.error('❌ 解析失败：', error.message);
}

// 示例2：处理非法JSON字符串
const badJsonString = '{ name: "Bob" }'; // 缺少引号，非法JSON

try {
  const result = JSON.parse(badJsonString);
} catch (error) {
  console.log('⚠️ 错误输入处理完成：无效的JSON字符串');
}