/**
 * 主服务器文件 - 使用Express和Multer处理文件上传
 */
const express = require('express');
const multer = require('multer');
const path = require('path');
const upload = require('./upload');

const app = express();
const PORT = 3000;

// 静态文件服务：提供HTML表单页面
app.use(express.static('public'));

// 单文件上传路由
app.post('/upload', upload.single('file'), (req, res) => {
  // req.file 包含上传的文件信息
  if (!req.file) {
    return res.status(400).json({ error: '未选择文件' });
  }

  console.log(`收到文件: ${req.file.originalname}, 大小: ${req.file.size} 字节`);

  res.json({
    message: '文件上传成功',
    filename: req.file.filename,
    size: req.file.size,
    path: req.file.path
  });
});

// 多文件上传路由
app.post('/uploads', upload.array('files', 5), (req, res) => {
  // 最多允许上传5个文件
  if (!req.files || req.files.length === 0) {
    return res.status(400).json({ error: '未选择任何文件' });
  }

  console.log(`共收到 ${req.files.length} 个文件`);

  const fileInfo = req.files.map(file => ({
    filename: file.filename,
    size: file.size,
    mimetype: file.mimetype
  }));

  res.json({
    message: '多文件上传成功',
    files: fileInfo
  });
});

// 启动服务器
app.listen(PORT, () => {
  console.log(`服务器运行在 http://localhost:${PORT}`);
  console.log(`上传页面可通过 http://localhost:${PORT} 访问`);
});