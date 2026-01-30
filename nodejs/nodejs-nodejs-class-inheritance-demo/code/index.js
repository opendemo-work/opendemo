/**
 * index.js - 主执行文件
 * 实例化类并测试继承功能
 */

// 引入定义好的类
const { Dog, Cat } = require('./animal');
const { Manager } = require('./employee');

// 示例1：测试动物类继承
const dog = new Dog('旺财');
dog.makeSound(); // 输出: 🐕 狗叫: 汪汪！

const cat = new Cat('咪咪');
cat.makeSound(); // 输出: 🐱 猫叫: 喵喵！

// 示例2：测试员工类继承
const manager = new Manager('张伟', '技术部', 5);
console.log(manager.getDetails()); // 输出: 💼 经理姓名: 张伟，部门: 技术部，团队人数: 5