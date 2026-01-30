import express, { Request, Response, NextFunction } from 'express';

// 扩展Express的Request类型，加入自定义属性
export interface RequestWithTime extends Request {
  requestTime: number;
}

// 创建Express应用实例
const app = express();
const PORT = process.env.PORT || 3000;

// 中间件：记录每个请求的时间戳
app.use((req: RequestWithTime, res: Response, next: NextFunction) => {
  req.requestTime = Date.now(); // 注入时间戳
  console.log(`[${new Date(req.requestTime).toISOString()}] ${req.method} ${req.url}`);
  next(); // 继续处理下一个中间件或路由
});

// 路由：GET /api/hello
app.get('/api/hello', (req: RequestWithTime, res: Response) => {
  // 返回JSON格式响应，包含消息和时间戳
  res.json({
    message: 'Hello from TypeScript!',
    timestamp: req.requestTime
  });
});

// 导出app以便在server.ts中使用
export default app;