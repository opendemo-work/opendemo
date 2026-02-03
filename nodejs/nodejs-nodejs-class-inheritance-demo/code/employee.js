/**
 * employee.js - 员工管理系统类示例
 * 展示属性扩展与方法重写
 */

class Employee {
  constructor(name, position) {
    this.name = name;
    this.position = position;
  }

  getDetails() {
    return `员工姓名: ${this.name}，职位: ${this.position}`;
  }
}

// Manager 继承 Employee 并扩展功能
class Manager extends Employee {
  constructor(name, department, teamSize) {
    // 必须首先调用 super() 来初始化父类部分
    super(name, '经理');
    this.department = department;
    this.teamSize = teamSize;
  }

  // 重写方法以包含更多细节
  getDetails() {
    return `💼 经理姓名: ${this.name}，部门: ${this.department}，团队人数: ${this.teamSize}`;
  }
}

module.exports = { Employee, Manager };