# Spring MVC Web开发演示

> 构建RESTful API的完整指南

## 🎯 学习目标

- ✅ 理解Spring MVC架构
- ✅ 掌握@Controller和@RestController
- ✅ 学会请求映射和参数绑定
- ✅ 掌握RESTful API设计

---

## 📚 RESTful API端点

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | /api/users | 获取所有用户 |
| GET | /api/users/{id} | 根据ID获取用户 |
| POST | /api/users | 创建用户 |
| PUT | /api/users/{id} | 更新用户 |
| DELETE | /api/users/{id} | 删除用户 |

---

## 💻 核心代码

### Controller

```java
@RestController
@RequestMapping("/api/users")
public class UserController {
    
    @GetMapping
    public List<User> getAllUsers() {
        return userService.findAll();
    }
    
    @GetMapping("/{id}")
    public User getUserById(@PathVariable Long id) {
        return userService.findById(id);
    }
    
    @PostMapping
    public User createUser(@RequestBody User user) {
        return userService.createUser(user);
    }
}
```

---

## 🚀 运行

```bash
mvn clean package
# 部署到Tomcat
```

---

*最后更新：2026年4月*
