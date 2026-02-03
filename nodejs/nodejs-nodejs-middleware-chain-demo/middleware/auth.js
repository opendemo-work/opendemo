/**
 * 认证中间件：验证请求是否包含有效令牌
 * 演示条件判断与流程终止
 * @param {Object} req - Express请求对象
 * @param {Object} res - Express响应对象
 * @param {Function} next - 控制流转到下一个中间件
 */
function auth(req, res, next) {
  // 从请求头获取Authorization字段
  const authHeader = req.headers['authorization'];

  // 检查是否存在且以'Bearer '开头
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    // 条件不满足：返回401并结束响应流程
    // 注意：此时不调用next()，阻止继续向下执行
    return res.status(401).json({ error: '未提供认证令牌' });
  }

  // 模拟令牌验证成功
  // 可在此处添加JWT解析或数据库查询逻辑
  console.log('认证通过:', authHeader);

  // 附加用户信息到请求对象（模拟解码后的payload）
  req.user = { id: 1, name: 'test-user' };

  // 继续执行后续中间件或路由处理器
  next();
}

module.exports = auth;