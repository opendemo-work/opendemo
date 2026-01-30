/**
 * 响应式数据系统：基于Proxy的简易实现
 * 模拟Vue的响应式原理
 */

// 存储副作用函数
const effects = [];

// 注册副作用
function effect(fn) {
  effects.push(fn);
  fn(); // 立即执行一次
}

// 目标状态
const state = {
  name: 'Alice',
  age: 25
};

// 创建响应式对象
const reactiveState = new Proxy(state, {
  set(target, property, value, receiver) {
    const result = Reflect.set(target, property, value, receiver);
    
    // 触发所有副作用
    console.log(`${property} 更新为：${value}`);
    effects.forEach(effectFn => effectFn());
    
    return result;
  }
});

// 定义副作用（类似watcher）
effect(() => {
  // 这里可以触发视图更新等操作
  if (reactiveState.name) {/* 模拟使用 */}
});

effect(() => {
  if (reactiveState.age) {/* 模拟使用 */}
});

// 修改数据测试响应性
setTimeout(() => {
  reactiveState.name = 'Charlie';
}, 100);

setTimeout(() => {
  reactiveState.age = 31;
}, 200);