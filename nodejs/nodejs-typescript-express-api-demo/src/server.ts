import app from './app';

const PORT = process.env.PORT || 3000;

// 启动服务器并监听指定端口
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
  console.log(`Try visiting: http://localhost:${PORT}/api/hello`);
});