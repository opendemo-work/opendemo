// nested-callbacks.js - 嵌套回调示例（回调地狱雏形）

function stepOne(callback) {
  setTimeout(() => {
    console.log('第一步完成：准备数据');
    callback(null, 'DATA_READY');
  }, 300);
}

function stepTwo(data, callback) {
  setTimeout(() => {
    console.log('第二步完成：处理数据');
    const processed = `${data}_PROCESSED`;
    callback(null, processed);
  }, 300);
}

function stepThree(data, callback) {
  setTimeout(() => {
    console.log('第三步完成：生成结果');
    const result = `${data}_FINAL`;
    callback(null, result);
  }, 300);
}

// 执行三个步骤（嵌套回调）
stepOne((err, result1) => {
  if (err) return console.error(err);
  stepTwo(result1, (err, result2) => {
    if (err) return console.error(err);
    stepThree(result2, (err, finalResult) => {
      if (err) return console.error(err);
      console.log('最终结果：', finalResult.replace('_FINAL', ''));
    });
  });
});