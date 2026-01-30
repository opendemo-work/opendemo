/**
 * 日志中间件：记录每个请求的基本信息
 * @param {Object} req - Express请求对象
 * @param {Object} res - Express响应对象
 * @param {Function} next - 控制流转到下一个中间件
 */
function logger(req, res, next) {
  // 记录请求时间戳和基本信息
  const timestamp = new Date().toISOString();
  console.log(`[${timestamp}] ${req.method} ${req.url}`);

  // 将自定义数据附加到请求对象，供后续中间件使用
  req.requestTime = timestamp;

  // 调用next()以继续执行中间件链
  // 如果不调用，请求将在此处挂起
  next();
}

module.exports = logger;