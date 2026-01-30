// =========================================
// 文件名: json-file-io.js
// 功能: 演示JSON文件的读写操作
// 使用Node.js内置fs模块（无需安装依赖）
// 最佳实践: 同步操作用于脚本，生产环境建议异步
// =========================================

const fs = require('fs');

// 要写入的数据对象
const dataToSave = {
  id: 1,
  message: 'Hello from JSON file!'
};

// 文件路径
const filePath = './data.json';

// === 写入JSON文件 ===
try {
  // 将对象序列化为带缩进的JSON字符串
  const jsonData = JSON.stringify(dataToSave, null, 2) + '\n';
  
  // 同步写入文件
  fs.writeFileSync(filePath, jsonData, 'utf8');
  console.log('📄 数据已写入', filePath);
} catch (error) {
  console.error('写入文件失败：', error.message);
}

// === 读取JSON文件 ===
try {
  console.log('💾 正在读取', filePath + '...');
  
  // 同步读取文件内容（字符串）
  const rawContent = fs.readFileSync(filePath, 'utf8');
  
  // 解析JSON字符串为对象
  const parsedData = JSON.parse(rawContent);
  console.log('🔍 读取并解析成功：', parsedData);
} catch (error) {
  if (error.code === 'ENOENT') {
    console.error('❌ 文件不存在，请先运行写入操作');
  } else if (error instanceof SyntaxError) {
    console.error('❌ JSON格式错误，请检查文件内容');
  } else {
    console.error('❌ 读取失败：', error.message);
  }
}