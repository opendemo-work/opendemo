// advanced-usage.js
// 高级模板字符串用法：表达式与多行文本

// 示例1：在模板字符串中直接执行表达式
const a = 3;
const b = 5;
const resultMessage = `计算结果：${a} + ${b} = ${a + b}`;
console.log(resultMessage);

// 示例2：生成多行HTML结构
// 模板字符串天然支持换行，非常适合生成HTML或配置文件
const title = '欢迎';
const content = '这是内容';
const html = `<div>
  <h1>${title}</h1>
  <p>${content}</p>
</div>`;

console.log(`生成的HTML：${html}`);

// 注意：缩进会保留，若需格式化可使用专门的HTML模板库