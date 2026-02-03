/**
 * 演示箭头函数与普通函数在 this 绑定上的差异
 */

const person = {
  name: '张三',
  // 普通函数：this 在运行时绑定
  introduce: function() {
    console.log('普通函数中的 this.name:', this.name);
  },
  // 箭头函数：继承定义时的 this 上下文
  introduceArrow: () => {
    console.log('箭头函数中的 this.name:', this.name);
  },
  // 在 setTimeout 中正确使用箭头函数
  delayedIntroduction: function() {
    setTimeout(() => {
      console.log('延迟输出 - 箭头函数:', this.name); // 能正确访问 person.name
    }, 100);
  },
  // 普通函数在 setTimeout 中会丢失 this
  delayedIntroductionOld: function() {
    const self = this; // 传统解决方案
    setTimeout(function() {
      console.log('延迟输出 - 传统函数:', self.name);
    }, 100);
  }
};

// 执行测试
if (require.main === module) {
  person.introduce();               // 输出: 张三
  person.introduceArrow();          // 输出: undefined (顶层 this.name)
  person.delayedIntroduction();     // 输出: 张三
  person.delayedIntroductionOld();  // 输出: 张三
}

module.exports = person;