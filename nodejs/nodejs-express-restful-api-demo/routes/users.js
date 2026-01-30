// 使用 express.Router() 创建一个可挂载的路由实例
const express = require('express');
const router = express.Router();

// 模拟数据库：使用数组存储用户数据（仅用于演示）
// 实际项目中应替换为数据库如 MongoDB、MySQL 等
let users = [
  { id: 1, name: '张三', email: 'zhangsan@example.com' }
];

// 当前最大 ID，用于生成新用户的唯一 ID
let nextId = 2;

// GET /users - 获取所有用户
// 符合 RESTful 规范：使用名词复数表示资源集合
router.get('/', (req, res) => {
  // 返回 JSON 格式的用户列表
  res.json(users);
});

// POST /users - 创建一个新用户
// 接收 JSON 请求体，验证必要字段，并添加到列表中
router.post('/', (req, res) => {
  const { name, email } = req.body;

  // 基础输入验证
  if (!name || !email) {
    return res.status(400).json({ error: '姓名和邮箱是必填项' });
  }

  // 创建新用户对象
  const newUser = {
    id: nextId++,
    name,
    email
  };

  // 添加到用户数组
  users.push(newUser);

  // 返回 201 Created 状态码和新用户数据
  res.status(201).json(newUser);
});

// PUT /users/:id - 更新指定 ID 的用户
// :id 是路由参数，通过 req.params.id 访问
router.put('/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const { name, email } = req.body;

  // 查找对应用户
  const user = users.find(u => u.id === id);
  if (!user) {
    return res.status(404).json({ error: '用户未找到' });
  }

  // 更新信息
  user.name = name;
  user.email = email;

  // 返回更新后的用户
  res.json(user);
});

// DELETE /users/:id - 删除指定用户
router.delete('/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const index = users.findIndex(u => u.id === id);

  // 若未找到用户，返回 404
  if (index === -1) {
    return res.status(404).json({ error: '用户未找到' });
  }

  // 从数组中移除该用户
  users.splice(index, 1);

  // 返回 204 No Content，表示删除成功且无内容返回
  res.status(204).send();
});

// 导出路由实例，供 app.js 引入使用
module.exports = router;