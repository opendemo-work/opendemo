// models/User.js
// 定义用户数据模型

const mongoose = require('mongoose');

// 定义用户 Schema，描述数据结构和约束
const userSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,  // 名称必填
    trim: true      // 自动去除首尾空格
  },
  age: {
    type: Number,
    min: 0,         // 年龄不能为负
    max: 120
  }
}, {
  timestamps: true  // 自动添加 createdAt 和 updatedAt 字段
});

// 创建 User 模型，对应 MongoDB 中的 users 集合
const User = mongoose.model('User', userSchema);

module.exports = User;