/**
 * 函数与嵌套对象代理：实现调用日志与路径追踪
 */

// 模拟服务对象
const apiService = {
  greet(name) {
    return `Hello, ${name}!`;
  },
  calc: {
    sum(a, b) {
      return a + b;
    }
  }
};

// 通用日志代理处理器
function createLoggerProxy(obj, path = '') {
  return new Proxy(obj, {
    get(target, property) {
      const value = target[property];
      const currentPath = path ? `${path}.${property}` : property;

      // 如果是函数，包装它
      if (typeof value === 'function') {
        return new Proxy(value, {
          apply(fn, thisArg, args) {
            console.log(`调用 '${currentPath}', 参数长度: ${args.length}`);
            const result = Reflect.apply(fn, thisArg, args);
            console.log(`执行原始函数：${result}`);
            return result;
          }
        });
      }

      // 如果是对象，递归代理
      if (value && typeof value === 'object') {
        return createLoggerProxy(value, currentPath);
      }

      // 普通属性直接返回
      return value;
    }
  });
}

// 创建带日志的代理
const loggedApi = createLoggerProxy(apiService);

// 测试函数调用
loggedApi.greet('Bob');
loggedApi.calc.sum(2, 3);