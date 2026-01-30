/**
 * 示例3：使用闭包模拟事件处理器
 * 
 * 说明：常见于DOM事件监听、定时器等场景
 * 每个处理器都保留对其创建时环境的引用（如 buttonId 和 clickCount）
 */

// 模拟创建一个点击处理器，常用于按钮点击事件
function createClickHandler(buttonId) {
  // 每个处理器维护自己的点击次数
  let clickCount = 0;

  // 返回的处理函数形成闭包，捕获 buttonId 和 clickCount
  return function() {
    clickCount++;
    console.log(`按钮 ${buttonId} 被点击了 ${clickCount} 次`);
  };
}

// 创建多个按钮的事件处理器
const handler1 = createClickHandler(1);
const handler2 = createClickHandler(2);

// 模拟用户点击行为
handler1(); // 按钮1被点击
handler2(); // 按钮2被点击
handler1(); // 按钮1再次被点击
handler1(); // 按钮1第三次被点击