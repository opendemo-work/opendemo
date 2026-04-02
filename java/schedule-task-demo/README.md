# Schedule Task Demo

定时任务演示项目，演示Spring Boot的@Scheduled注解使用。

## 技术栈

- Spring Boot 2.7
- @Scheduled

## 定时任务类型

- fixedRate: 固定频率执行
- fixedDelay: 固定延迟执行
- cron: Cron表达式执行

## Cron表达式

```
秒 分 时 日 月 周
0 0 12 * * ?  # 每天12点
0 */5 * * * ? # 每5分钟
```
