/**
 * progressive-loader.js
 * 分步加载器示例
 * 展示如何通过Generator实现带进度反馈的异步流程
 */

// 模拟不同耗时的加载步骤
function loadUserData() {
  return new Promise(resolve => {
    setTimeout(() => resolve({ data: 'user_data', progress: 30 }), 800);
  });
}

function loadConfigFile() {
  return new Promise(resolve => {
    setTimeout(() => resolve({ data: 'config_data', progress: 60 }), 600);
  });
}

function initUI() {
  return new Promise(resolve => {
    setTimeout(() => resolve({ data: 'ui_ready', progress: 100 }), 400);
  });
}

// Generator实现分步加载流程
function* loadingProcess() {
  const steps = ['加载用户数据', '加载配置文件', '初始化界面'];
  
  for (let i = 0; i < steps.length; i++) {
    console.log(`[步骤${i+1}/${steps.length}] ${steps[i]}...`);
    
    // yield等待异步操作并获取进度信息
    const result = yield stepLoader(i);
    console.log(`完成 (${result.progress}%)`);
  }
  
  return '加载完成！';
}

// 根据步骤索引调用相应加载函数
function stepLoader(stepIndex) {
  const loaders = [loadUserData, loadConfigFile, initUI];
  return loaders[stepIndex]();
}

// 自定义运行器，处理进度反馈
function execute(generator) {
  const iterator = generator();
  
  function next(data) {
    const result = iterator.next(data);
    
    if (result.done) {
      console.log(result.value);
      return;
    }
    
    // 继续执行并传递结果
    result.value.then(next);
  }
  
  next();
}

// 运行加载流程
console.log('开始分步加载...');
execute(loadingProcess);