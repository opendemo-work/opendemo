/**
 * user.controller.ts - 用户控制器
 * 
 * 功能：处理HTTP请求，定义路由
 * 控制器负责接收客户端请求，调用服务层处理业务，并返回响应
 */

import { Controller, Get } from '@nestjs/common';
import { UserService } from './user.service';

/**
 * UserController - 定义/users路径下的API
 * @Controller('users') 表示该控制器下所有路由以 /users 开头
 */
@Controller('users')
export class UserController {
  // 依赖注入UserService实例
  constructor(private readonly userService: UserService) {}

  /**
   * 处理GET /users 请求
   * @returns 所有用户列表
   * 
   * 使用@Get()装饰器映射HTTP GET方法
   */
  @Get()
  getUsers() {
    return this.userService.findAll();
  }

  /**
   * 可扩展：添加POST /users 等其他方法
   */
}