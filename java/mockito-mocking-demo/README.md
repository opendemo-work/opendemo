# Mockito Mocking Demo

Mockito Mock测试演示项目，演示如何使用Mockito进行单元测试。

## 技术栈

- Spring Boot 2.7
- JUnit 5
- Mockito 4.x
- AssertJ

## 项目结构

```
mockito-mocking-demo/
├── src/main/java/com/example/demo/
│   ├── MockitoDemoApplication.java        # 应用入口
│   ├── model/
│   │   └── User.java                      # 用户实体
│   ├── repository/
│   │   └── UserRepository.java            # 用户仓库接口
│   └── service/
│       ├── UserService.java               # 用户服务
│       └── NotificationService.java       # 通知服务接口
├── src/test/java/com/example/demo/
│   └── service/
│       └── UserServiceTest.java           # 用户服务测试
├── pom.xml
└── README.md
```

## 什么是Mock

Mock是在测试过程中创建一个虚拟对象来替代真实对象。Mock对象可以：
- 模拟真实对象的行为
- 验证方法调用
- 隔离被测单元

## 为什么需要Mock

```
测试UserService时:

UserService ──▶ UserRepository (数据库)
           ──▶ NotificationService (邮件服务器)

问题:
1. 需要真实数据库
2. 需要邮件服务器
3. 测试慢且不稳定

解决方案 - Mock:
UserService ──▶ Mock UserRepository
           ──▶ Mock NotificationService
```

## 核心注解说明

### @Mock
创建Mock对象。

```java
@Mock
private UserRepository userRepository;
```

### @InjectMocks
自动将Mock对象注入到被测类中。

```java
@InjectMocks
private UserService userService;
```

### @ExtendWith(MockitoExtension.class)
启用Mockito JUnit5扩展。

```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest { }
```

## 快速开始

### 运行测试

```bash
# 运行所有测试
mvn test

# 运行单个测试类
mvn test -Dtest=UserServiceTest
```

## 核心API

### when/then - 配置Mock行为

```java
// 返回固定值
when(userRepository.findById(1L)).thenReturn(Optional.of(user));

// 抛出异常
when(userRepository.findById(999L)).thenThrow(new RuntimeException());

// 连续返回不同值
when(userRepository.findById(1L))
    .thenReturn(Optional.of(user))
    .thenReturn(Optional.empty());

// 使用参数匹配器
when(userRepository.existsByEmail(anyString())).thenReturn(false);
```

### verify - 验证方法调用

```java
// 验证方法被调用一次
verify(userRepository).findById(1L);

// 验证调用次数
verify(userRepository, times(3)).findById(anyLong());
verify(userRepository, never()).save(any());
verify(userRepository, atLeastOnce()).findAll();
verify(userRepository, atMost(5)).findById(anyLong());

// 验证调用顺序
InOrder inOrder = inOrder(userRepository);
inOrder.verify(userRepository).findById(1L);
inOrder.verify(userRepository).save(any(User.class));
```

### ArgumentCaptor - 参数捕获

```java
// 捕获参数
ArgumentCaptor<User> userCaptor = ArgumentCaptor.forClass(User.class);
verify(userRepository).save(userCaptor.capture());

// 获取捕获的值
User savedUser = userCaptor.getValue();
assertThat(savedUser.getUsername()).isEqualTo("john");
```

### Spy - 部分Mock

```java
// Spy会调用真实方法，除非被stub
List<String> spyList = spy(new ArrayList<>());
spyList.add("one");  // 调用真实方法
when(spyList.size()).thenReturn(100);  // stub方法
```

## 测试示例

### 基础Mock测试

```java
@Test
@DisplayName("根据ID获取用户")
void testGetUserById() {
    // given
    when(userRepository.findById(1L)).thenReturn(Optional.of(testUser));
    
    // when
    Optional<User> result = userService.getUserById(1L);
    
    // then
    assertThat(result).isPresent();
    assertThat(result.get().getUsername()).isEqualTo("john");
    verify(userRepository).findById(1L);
}
```

### 异常测试

```java
@Test
@DisplayName("邮箱已存在应抛出异常")
void testRegisterUser_EmailExists() {
    // given
    when(userRepository.existsByEmail(anyString())).thenReturn(true);
    
    // when & then
    assertThatThrownBy(() -> userService.registerUser(testUser))
            .isInstanceOf(IllegalArgumentException.class)
            .hasMessageContaining("邮箱已存在");
    
    verify(userRepository, never()).save(any());
}
```

### 参数匹配器

```java
// 任意参数
when(userRepository.save(any(User.class))).thenReturn(user);

// 任意字符串
when(userRepository.findByUsername(anyString())).thenReturn(Optional.empty());

// 任意Long
when(userRepository.findById(anyLong())).thenReturn(Optional.empty());

// eq - 匹配特定值
when(userRepository.findById(eq(1L))).thenReturn(Optional.of(user));

// 复杂匹配器
when(userRepository.save(argThat(u -> u.getAge() >= 18)))
    .thenReturn(user);
```

### 验证交互

```java
@Test
void testVerifyInteractions() {
    // 执行被测方法
    userService.registerUser(user);
    
    // 验证所有期望的交互
    verify(userRepository).existsByEmail("john@example.com");
    verify(userRepository).save(any(User.class));
    verify(notificationService).sendWelcomeEmail(any(User.class));
    
    // 验证没有其他交互
    verifyNoMoreInteractions(userRepository);
}
```

## Mock与Spy对比

| 特性 | Mock | Spy |
|------|------|-----|
| 真实方法 | 不调用 | 调用 |
| 用途 | 完全模拟依赖 | 部分模拟真实对象 |
| 创建方式 | mock(Class.class) | spy(realObject) |
| 典型场景 | Repository、Service | 验证真实对象的方法调用 |

## 最佳实践

### 1. 一个测试验证一个概念

```java
// 好 - 清晰单一
@Test
void shouldThrowExceptionWhenEmailExists() { }

// 不好 - 验证太多
@Test
void testUserService() { 
    // 测试了注册、更新、删除...
}
```

### 2. 使用@DisplayName

```java
@Test
@DisplayName("注册用户时邮箱已存在应抛出异常")
void shouldThrowExceptionWhenEmailExists() { }
```

### 3. 验证行为而不仅是状态

```java
// 不仅验证返回值，还要验证交互
@Test
void testRegister() {
    User result = userService.registerUser(user);
    
    // 状态验证
    assertThat(result.getId()).isNotNull();
    
    // 行为验证
    verify(notificationService).sendWelcomeEmail(user);
}
```

### 4. 不要过度使用Mock

```java
// 不要Mock值对象
User user = mock(User.class);  // 不好

User user = new User();  // 好
```

## BDD风格

```java
import static org.mockito.BDDMockito.*;

@Test
void testWithBDD() {
    // given
    given(userRepository.findById(1L)).willReturn(Optional.of(user));
    
    // when
    Optional<User> result = userService.getUserById(1L);
    
    // then
    assertThat(result).isPresent();
    then(userRepository).should().findById(1L);
}
```

## 学习要点

1. Mock的基本概念和用途
2. @Mock和@InjectMocks的使用
3. when/then配置Mock行为
4. verify验证方法调用
5. ArgumentCaptor捕获参数
6. Mock与Spy的区别和使用场景
7. 参数匹配器的使用
8. 单元测试最佳实践
