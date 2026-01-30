/**
 * 基础Proxy示例：拦截对象属性访问
 * 展示get/set/apply陷阱的使用
 */

// 目标对象
const user = {
  name: 'Alice',
  age: 25,
  getAge() {
    return this.age;
  }
};

// 代理处理器
const handler = {
  // 拦截属性读取
  get(target, property, receiver) {
    console.log(`读取属性 '${property}' ->`, target[property] !== undefined ? '返回值' : '未定义');
    // 使用Reflect保持默认行为
    return Reflect.get(target, property, receiver);
  },

  // 拦截属性设置（实现只读）
  set(target, property, value, receiver) {
    console.log(`尝试写入属性 '${property}'`);
    if (property === 'name') {
      console.warn('警告：禁止修改只读属性 \'' + property + '\'');
      return false; // 拒绝修改
    }
    return Reflect.set(target, property, value, receiver);
  },

  // 拦截函数调用
  apply(target, thisArg, argumentsList) {
    console.log(`调用方法 ${target.name || 'anonymous'}(), 参数个数: ${argumentsList.length}`);
    return Reflect.apply(target, thisArg, argumentsList);
  }
};

// 创建代理对象
const proxyUser = new Proxy(user, handler);
const proxyGetAge = new Proxy(user.getAge, handler);

// 测试行为
console.log(proxyUser.name); // 触发get
console.log(proxyGetAge());   // 触发apply
proxyUser.name = 'New Name'; // 触发set（被阻止）