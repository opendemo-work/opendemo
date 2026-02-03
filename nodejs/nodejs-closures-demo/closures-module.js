/**
 * 示例2：使用闭包实现模块模式
 * 
 * 说明：模拟面向对象中的私有属性和公共方法
 * 通过闭包隐藏敏感数据（如密码），只暴露安全的操作接口
 */

function createUser(name, pwd) {
  // 私有变量 - 外部无法直接访问
  let username = name;
  const password = pwd; // 假设这是加密后的密码

  // 返回一个包含公共方法的对象，这些方法共享同一个闭包环境
  return {
    // 获取用户名
    getName: () => username,
    
    // 修改用户名
    setName: (newName) => {
      if (typeof newName === 'string' && newName.length > 0) {
        username = newName;
        console.log('更新用户名成功');
      } else {
        throw new Error('用户名必须是非空字符串');
      }
    },
    
    // 提供有限的信息（比如密码长度），但不暴露原始值
    checkPasswordLength: () => password.length,
    
    // 注意：没有提供获取密码的方法，保证安全性
  };
}

// 创建用户实例
const user = createUser('Alice', 'secret');

// 使用公共接口操作
console.log(`用户名: ${user.getName()}`);
console.log(`密码长度: ${user.checkPasswordLength()}`);

user.setName('Bob');
console.log(`新用户名: ${user.getName()}`);

// 尝试直接访问私有变量（将返回 undefined）
console.log(`尝试直接访问密码: ${user.password}`);