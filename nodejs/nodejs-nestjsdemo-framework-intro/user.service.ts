/**
 * user.service.ts - 用户服务层
 * 
 * 功能：封装用户相关业务逻辑
 * 使用@Injectable()标记为可被依赖注入的服务
 * 在实际项目中，这里会调用数据库或外部API
 */

import { Injectable } from '@nestjs/common';

/**
 * UserService - 提供用户数据操作方法
 * 目前使用内存数组模拟数据存储
 */
@Injectable()
export class UserService {
  // 模拟用户数据
  private users = ['Alice', 'Bob'];

  /**
   * 获取所有用户
   * @returns string[] 用户名列表
   */
  findAll(): string[] {
    return this.users;
  }

  /**
   * 可扩展：添加新用户
   * @param name 用户名
   */
  // addUser(name: string) {
  //   this.users.push(name);
  // }
}