# Prompt 01: Proto 文件定义

创建 user.proto 文件，定义：
- package proto
- service UserService { rpc GetUser(GetUserRequest) returns(User) }
- message GetUserRequest { int32 id = 1 }
- message User { int32 id = 1; string name = 2; string email = 3 }

---
## 背景
- 工具：Claude Code（终端模式）
- 阶段：第 1 轮
- 结果：正确的 proto 文件
