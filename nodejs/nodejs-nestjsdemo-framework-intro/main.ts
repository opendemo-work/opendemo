/**
 * main.ts - NestJS应用入口文件
 * 
 * 功能：创建并启动Nest应用实例
 * 使用NestFactory.create()初始化应用，并监听指定端口
 */

// 导入核心模块
import { NestFactory } from '@nestjs/core';
import { Controller, Get, Module } from '@nestjs/common';
import { UserService } from './user.service';
import { UserController } from './user.controller';

/**
 * AppModule - 根模块
 * 在NestJS中，每个应用至少有一个模块（Module），即根模块
 * @Module装饰器用于组织控制器和服务
 */
@Module({
  imports: [],
  controllers: [UserController],
  providers: [UserService],
})
export class AppModule {}

/**
 * 异步启动函数
 * 创建Nest应用实例并监听3000端口
 */
async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  await app.listen(3000);
  console.log('🚀 应用程序正在 http://localhost:3000 上运行');
}
bootstrap(); // 启动应用