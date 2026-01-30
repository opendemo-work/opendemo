# NodeJS类继承演示

## 简介
本演示项目展示了在Node.js环境中如何使用ES6的类（class）和继承（inheritance）机制。通过两个具体场景——基础动物类与子类、员工管理系统，帮助开发者理解面向对象编程在JavaScript中的实现方式。

## 学习目标
- 理解ES6中`class`和`extends`关键字的使用
- 掌握`super()`在构造函数和方法重写中的作用
- 学会在子类中扩展和覆盖父类行为
- 遵循Node.js行业编码规范

## 环境要求
- Node.js 版本：14.x 或更高（推荐使用 LTS 版本，如 18.x 或 20.x）
- 操作系统：Windows、macOS、Linux 均支持
- 包管理器：npm（通常随Node.js自动安装）

## 安装依赖的详细步骤
由于本项目仅使用原生JavaScript功能，无需第三方依赖，只需确保Node.js已正确安装。

1. 打开终端（Terminal）或命令提示符
2. 运行以下命令检查Node.js版本：
   ```bash
   node -v
   ```
   预期输出（版本号可能不同）：
   ```
   v18.17.0
   ```
3. 确保npm可用：
   ```bash
   npm -v
   ```
   预期输出：
   ```
   9.6.7
   ```

## 文件说明
- `animal.js`：定义基础Animal类及Dog和Cat子类，展示基本继承机制
- `employee.js`：实现Employee基类与Manager子类，演示属性扩展与方法重写
- `index.js`：主入口文件，运行并测试所有类的功能

## 逐步实操指南

1. 创建项目目录并进入：
   ```bash
   mkdir class-inheritance-demo && cd class-inheritance-demo
   ```

2. 初始化npm项目（可选，用于结构化管理）：
   ```bash
   npm init -y
   ```

3. 将以下三个文件内容复制到对应路径：
   - `animal.js`
   - `employee.js`
   - `index.js`

4. 在项目根目录运行主程序：
   ```bash
   node index.js
   ```

### 预期输出
```bash
🐕 狗叫: 汪汪！\n🐱 猫叫: 喵喵！\n💼 经理姓名: 张伟，部门: 技术部，团队人数: 5\n```

## 代码解析

### animal.js
```js
// 使用class关键字定义基础类
// 子类通过extends继承父类，并用super调用父类构造函数
// 方法重写体现多态性
```

### employee.js
```js
// Manager类扩展了Employee的功能
// super()在构造函数中必须在this之前调用
// getDetails()方法被重写以包含额外信息
```

### index.js
```js
// 实例化子类对象并调用继承/重写的方法
// 展示多态性和代码复用优势
```

## 常见问题解答

**Q: 为什么在子类构造函数中必须先调用super()？**
A: 因为子类需要先初始化父类的实例部分，才能安全地访问this。

**Q: 可以不使用class而用函数模拟继承吗？**
A: 可以，但ES6 class语法更清晰、易读，是当前行业标准。

**Q: 如何实现多重继承？**
A: JavaScript不支持多重继承。可通过Mixin模式或组合替代。

## 扩展学习建议
- 学习JavaScript原型链（prototype chain）机制
- 探索TypeScript中的类与接口，更适合大型OOP项目
- 阅读《You Don't Know JS》系列书籍深入理解JS面向对象