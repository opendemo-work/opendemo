// userModel.js - 用户数据模型定义

const { DataTypes } = require('sequelize');
const { sequelize } = require('./db');

// 定义 User 模型
// 对应数据库中的 users 表
const User = sequelize.define('User', {
  id: {
    type: DataTypes.INTEGER,
    autoIncrement: true,
    primaryKey: true
  },
  name: {
    type: DataTypes.STRING(100),
    allowNull: false,           // 名称不能为空
    validate: {
      len: [1, 100]           // 长度限制
    }
  },
  email: {
    type: DataTypes.STRING(255),
    allowNull: false,
    unique: true,               // 邮箱唯一
    validate: {
      isEmail: true            // 必须是合法邮箱格式
    }
  }
}, {
  tableName: 'users',         // 显式指定表名
  paranoid: false,              // 不启用软删除
  indexes: [
    {
      unique: true,
      fields: ['email']         // 为 email 字段添加唯一索引
    }
  ]
});

module.exports = User;