/**
 * buffer-string.js
 * 场景：字符串与 Buffer 的编码/解码转换
 * 展示 UTF-8 和 Base64 的使用
 */

// 定义原始字符串
const str = 'Hello, Buffer!';

// 将字符串编码为 UTF-8 Buffer
const bufferUtf8 = Buffer.from(str);
console.log('原始字符串:', str);
console.log('UTF-8 Buffer:', bufferUtf8);

// 将 Buffer 解码回字符串
const decodedStr = bufferUtf8.toString();
console.log('从 Buffer 解码:', decodedStr);

// 使用 Base64 编码字符串
const bufferBase64 = Buffer.from(str).toString('base64');
console.log('Base64 编码:', bufferBase64);

// 从 Base64 解码回字符串
const fromBase64 = Buffer.from(bufferBase64, 'base64').toString();
console.log('从 Base64 解码:', fromBase64);
