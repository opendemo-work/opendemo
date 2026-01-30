/**
 * animal.js - 动物类及其子类示例
 * 展示基础类继承与方法重写
 */

class Animal {
  constructor(name, species) {
    // 基础属性初始化
    this.name = name;
    this.species = species;
  }

  // 基类通用方法
  makeSound() {
    console.log(`${this.name} 发出了声音！`);
  }
}

// Dog 类继承 Animal
class Dog extends Animal {
  constructor(name) {
    // 调用父类构造函数
    super(name, '犬科');
  }

  // 重写父类方法
  makeSound() {
    console.log(`🐕 狗叫: 汪汪！`);
  }
}

// Cat 类继承 Animal
class Cat extends Animal {
  constructor(name) {
    super(name, '猫科');
  }

  makeSound() {
    console.log(`🐱 猫叫: 喵喵！`);
  }
}

// 导出类供其他模块使用
module.exports = { Animal, Dog, Cat };