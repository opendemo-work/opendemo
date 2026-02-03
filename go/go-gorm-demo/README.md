# GORM增删改查实战演示

## 简介
本项目是一个基于Go语言和GORM ORM框架的简单但完整的增删改查（CRUD）操作演示。使用SQLite作为后端数据库，无需额外配置即可运行，适合学习和教学使用。

## 学习目标
- 掌握GORM的基本初始化与连接数据库
- 学会使用GORM进行数据的创建、读取、更新和删除操作
- 理解模型定义与自动迁移机制
- 熟悉Go中结构体与数据库表的映射关系

## 环境要求
- Go 1.19 或更高版本
- 操作系统：Windows / Linux / macOS（均支持）
- 无其他外部依赖（SQLite为文件数据库）

## 安装依赖的详细步骤

1. 打开终端或命令行工具
2. 进入项目目录：
   ```bash
   cd path/to/your/project
   ```
3. 初始化Go模块（如果尚未初始化）：
   ```bash
   go mod init gorm-demo
   ```
4. 添加GORM依赖：
   ```bash
   go get gorm.io/gorm
   go get gorm.io/driver/sqlite
   ```

## 文件说明
- `main.go`：主程序文件，包含用户模型定义及完整的CRUD操作演示
- `go.mod`：Go模块依赖声明文件（由`go mod init`生成）

## 逐步实操指南

### 步骤1：创建项目目录并初始化
```bash
mkdir gorm-crud-demo && cd gorm-crud-demo
go mod init gorm-demo
```

### 步骤2：创建并编辑 main.go
将下面的内容保存为 `main.go` 文件。

### 步骤3：运行程序
```bash
go run main.go
```

### 预期输出
```
已连接到数据库
已自动创建表
✅ 创建用户：ID=1, 名字=Alice, 年龄=30
✅ 查询所有用户：
- 用户: ID=1, 名字=Alice, 年龄=30
✅ 更新用户年龄：ID=1 -> 新年龄=31
✅ 删除用户：ID=1
✅ 验证删除结果：当前用户总数 = 0
🎉 所有操作执行完成！
```

## 代码解析

### 模型定义
```go
type User struct {
  gorm.Model
  Name string
  Age  int
}
```
- `gorm.Model` 提供了ID、CreatedAt、UpdatedAt、DeletedAt等常用字段
- 结构体字段首字母大写以导出，GORM通过标签或约定映射到数据库列

### 自动迁移
```go
db.AutoMigrate(&User{})
```
- 若表不存在则自动创建，字段变更时也会尝试更新表结构（非生产推荐）

### CRUD操作
- **Create**: `db.Create(&user)`
- **Read**: `db.Find(&users)`
- **Update**: `db.Model(&user).Update("Age", 31)`
- **Delete**: `db.Delete(&user, user.ID)`

## 常见问题解答

**Q: 运行时报错找不到sqlite驱动？**
A: 确保已执行 `go get gorm.io/driver/sqlite`，并检查导入路径是否正确。

**Q: 能否使用MySQL或PostgreSQL？**
A: 可以，只需替换驱动为 `gorm.io/driver/mysql` 或 `postgresql`，并调整连接字符串。

**Q: DeletedAt是什么？**
A: GORM软删除机制，记录删除时间而非物理删除，可用 `Unscoped()` 查询含已删数据。

## 扩展学习建议
- 尝试添加更多字段如Email，并加验证
- 使用事务处理多个操作
- 探索关联关系（Has One, Has Many）
- 结合Gin框架构建REST API
- 使用`.First()`、`.Where()`等条件查询方法