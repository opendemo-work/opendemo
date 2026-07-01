<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Hibernate 实体映射演示项目

## 项目简介

本项目是一个基于 Spring Boot 2.7.12 的 Hibernate 实体映射演示应用，使用 Spring Data JPA 和 Hibernate 作为 ORM 框架，H2 作为内存数据库。项目展示了 JPA 中各种实体关系映射、嵌入式对象、级联操作、抓取策略等核心概念。

## 技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| Java | 11 | JDK 版本 |
| Spring Boot | 2.7.12 | 应用框架 |
| Spring Data JPA | - | 数据访问层框架 |
| Hibernate | - | JPA 实现 |
| H2 | Runtime | 内存数据库 |
| Maven | - | 构建工具 |

## 实体映射详解

### @OneToMany（一对多）

一对多关系是最常见的实体关系之一。在本项目中，`Department` 和 `Employee` 之间就是一对多关系：一个部门可以有多个员工。

```java
@Entity
public class Department {
    @OneToMany(mappedBy = "department", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Employee> employees = new ArrayList<>();
}
```

**关键配置说明**：
- `mappedBy = "department"` - 指定由 Employee 端的 `department` 属性维护关系
- `cascade = CascadeType.ALL` - 级联所有操作
- `orphanRemoval = true` - 自动删除孤儿记录

**双向维护的辅助方法**：

```java
public void addEmployee(Employee employee) {
    employees.add(employee);
    employee.setDepartment(this);
}

public void removeEmployee(Employee employee) {
    employees.remove(employee);
    employee.setDepartment(null);
}
```

在双向关系中，必须同时维护两端的关系，建议使用这样的辅助方法。

### @ManyToOne（多对一）

`@ManyToOne` 是 `@OneToMany` 的另一面。在本项目中，`Employee` 属于一个 `Department`。

```java
@Entity
public class Employee {
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "department_id")
    private Department department;
}
```

**关键配置说明**：
- `fetch = FetchType.LAZY` - 懒加载，访问时才查询
- `@JoinColumn(name = "department_id")` - 指定外键列名

### @ManyToMany（多对多）

多对多关系需要一个中间表。在本项目中，`Employee` 和 `Project` 之间就是多对多关系：一个员工可以参与多个项目，一个项目可以有多个员工。

```java
@Entity
public class Employee {
    @ManyToMany(fetch = FetchType.LAZY)
    @JoinTable(
        name = "employee_project",
        joinColumns = @JoinColumn(name = "employee_id"),
        inverseJoinColumns = @JoinColumn(name = "project_id")
    )
    private Set<Project> projects = new HashSet<>();
}

@Entity
public class Project {
    @ManyToMany(mappedBy = "projects", fetch = FetchType.LAZY)
    private Set<Employee> employees = new HashSet<>();
}
```

**关键配置说明**：
- `@JoinTable` - 定义中间表的名称和列
- `joinColumns` - 本实体在中间表中的外键列
- `inverseJoinColumns` - 对方实体在中间表中的外键列
- 使用 `Set` 而非 `List` 避免重复和效率问题

### @Embeddable（嵌入式对象）

`@Embeddable` 用于将一组属性封装为一个可复用的值类型。在本项目中，`Address` 被设计为嵌入式对象。

```java
@Embeddable
public class Address {
    @Column(name = "street", length = 200)
    private String street;
    @Column(name = "city", length = 100)
    private String city;
    @Column(name = "zip_code", length = 20)
    private String zipCode;
}

@Entity
public class Employee {
    @Embedded
    private Address address;
}
```

嵌入式对象不是独立的实体，它没有自己的主键，其属性会被映射到所属实体的表中。

## 级联类型（Cascade Types）

级联操作定义了当一个实体执行某个操作时，是否对其关联的实体也执行相同的操作。

### CascadeType.PERSIST

当保存父实体时，自动保存关联的子实体：

```java
Department dept = new Department("技术部");
Employee emp = new Employee("张三", "开发");
dept.addEmployee(emp);
departmentRepository.save(dept); // emp 也会被自动保存
```

### CascadeType.MERGE

当合并（更新）父实体时，自动合并关联的子实体。

### CascadeType.REMOVE

当删除父实体时，自动删除关联的子实体。

### CascadeType.ALL

包含所有级联操作：PERSIST、MERGE、REMOVE、REFRESH、DETACH。

### orphanRemoval

`orphanRemoval = true` 会自动删除不再与任何父实体关联的子实体：

```java
dept.removeEmployee(emp);
// 当 dept 保存时，emp 会被自动删除
```

## 抓取策略（Fetch Types）

### EAGER（立即加载）

当加载一个实体时，立即加载其关联的实体。

```java
@OneToMany(fetch = FetchType.EAGER)
private List<Employee> employees;
```

**特点**：
- 立即执行额外的 SELECT 语句
- 适合关联数据总是需要使用的场景
- 可能导致大量不必要的查询

### LAZY（懒加载）

当加载一个实体时，不加载其关联的实体，只有当实际访问关联属性时才执行查询。

```java
@OneToMany(fetch = FetchType.LAZY)
private List<Employee> employees;
```

**特点**：
- 延迟执行 SELECT 语句
- 默认推荐策略
- 需要在事务内使用或使用 DTO 投影
- 在 Session 关闭后访问会抛出 `LazyInitializationException`

### 推荐策略

| 关系类型 | 默认策略 | 推荐策略 |
|----------|----------|----------|
| @OneToMany | LAZY | LAZY |
| @ManyToOne | EAGER | LAZY |
| @ManyToMany | LAZY | LAZY |
| @OneToOne | EAGER | LAZY |

**通用建议**：所有关联都使用 LAZY，需要时通过 JOIN FETCH 显式加载。

## N+1 查询问题

### 什么是 N+1 问题

N+1 问题是 ORM 框架中最常见的性能问题之一。当加载 N 个父实体并逐一访问其懒加载的关联实体时，会执行 1 次查询加载父实体 + N 次查询加载每个父实体的关联实体，共 N+1 次查询。

### 示例

```java
List<Department> departments = departmentRepository.findAll(); // 1 次查询
for (Department dept : departments) {
    dept.getEmployees().size(); // 每个 department 1 次查询，共 N 次
}
```

### 解决方案

#### 1. JOIN FETCH

使用 JPQL 的 JOIN FETCH 一次性加载关联数据：

```java
@Query("SELECT d FROM Department d JOIN FETCH d.employees")
List<Department> findAllWithEmployees();
```

#### 2. @EntityGraph

使用 Entity Graph 定义加载计划：

```java
@EntityGraph(attributePaths = {"employees"})
List<Department> findAll();
```

#### 3. 批量抓取

在实体上配置批量抓取：

```java
@BatchSize(size = 50)
@OneToMany(mappedBy = "department")
private List<Employee> employees;
```

#### 4. DTO 投影

直接查询需要的数据，避免加载完整实体：

```java
@Query("SELECT new com.example.demo.dto.DepartmentDTO(d.id, d.name, COUNT(e)) " +
       "FROM Department d LEFT JOIN d.employees e GROUP BY d.id")
List<DepartmentDTO> findDepartmentDTOs();
```

## 实体生命周期

JPA 实体有以下生命周期状态和对应的回调注解：

### 生命周期状态

```
                    new()
                      |
                      v
              +---> Transient (新建)
              |        |
              |        | persist()
              |        v
    remove()  |   +---> Managed (托管)
       +------+   |        |
       |          |        | flush()/commit()
       |          |        v
       |    evict()   +---> DataSynchronized
       |       |          |
       v       v          |
     Removed   Detached <--+
     (删除)    (游离）
```

### 生命周期回调

```java
@Entity
public class Employee {
    @PrePersist
    public void prePersist() {
        // 实体持久化前调用
    }

    @PostPersist
    public void postPersist() {
        // 实体持久化后调用
    }

    @PreUpdate
    public void preUpdate() {
        // 实体更新前调用
    }

    @PostUpdate
    public void postUpdate() {
        // 实体更新后调用
    }

    @PreRemove
    public void preRemove() {
        // 实体删除前调用
    }

    @PostRemove
    public void postRemove() {
        // 实体删除后调用
    }

    @PostLoad
    public void postLoad() {
        // 实体从数据库加载后调用
    }
}
```

### 常见用途

- `@PrePersist` - 设置创建时间、初始状态
- `@PreUpdate` - 设置更新时间
- `@PostLoad` - 计算派生属性

## 项目结构

```
hibernate-entity-mapping-demo/
├── pom.xml                                        # Maven 项目配置
├── README.md                                      # 项目说明文档
├── metadata.json                                  # 项目元数据
└── src/
    ├── main/
    │   ├── java/com/example/demo/
    │   │   ├── HibernateMappingDemoApplication.java  # 应用启动类
    │   │   ├── entity/
    │   │   │   ├── Department.java                # 部门实体（@OneToMany）
    │   │   │   ├── Employee.java                  # 员工实体（@ManyToOne, @ManyToMany）
    │   │   │   ├── Project.java                   # 项目实体（@ManyToMany）
    │   │   │   └── Address.java                   # 地址值对象（@Embeddable）
    │   │   ├── repository/
    │   │   │   ├── DepartmentRepository.java      # 部门 Repository
    │   │   │   ├── EmployeeRepository.java        # 员工 Repository
    │   │   │   └── ProjectRepository.java         # 项目 Repository
    │   │   ├── service/
    │   │   │   └── CompanyService.java            # 业务逻辑层
    │   │   └── controller/
    │   │       └── CompanyController.java         # REST API 控制器
    │   └── resources/
    │       └── application.yml                    # 应用配置
    └── test/
        └── java/com/example/demo/
            └── HibernateMappingDemoApplicationTest.java  # 测试类
```

## 快速开始

### 环境要求

- JDK 11+
- Maven 3.6+

### 运行步骤

1. **克隆项目**

```bash
git clone <repository-url>
cd hibernate-entity-mapping-demo
```

2. **编译项目**

```bash
mvn clean compile
```

3. **运行测试**

```bash
mvn test
```

4. **启动应用**

```bash
mvn spring-boot:run
```

### API 测试示例

```bash
# 创建部门
curl -X POST http://localhost:8080/api/departments \
  -H "Content-Type: application/json" \
  -d '{"name":"技术部"}'

# 添加员工到部门
curl -X POST http://localhost:8080/api/departments/1/employees \
  -H "Content-Type: application/json" \
  -d '{"name":"张三","position":"开发工程师","address":{"street":"中关村","city":"北京","zipCode":"100080"}}'

# 创建项目
curl -X POST http://localhost:8080/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name":"核心系统","description":"核心业务系统开发"}'

# 分配员工到项目
curl -X POST http://localhost:8080/api/employees/1/projects/1

# 查看部门下的员工
curl http://localhost:8080/api/departments/1/employees

# 查看所有员工
curl http://localhost:8080/api/employees
```

## Hibernate 配置详解

### application.yml JPA 配置

```yaml
spring:
  jpa:
    hibernate:
      ddl-auto: create-drop
    show-sql: true
    properties:
      hibernate:
        dialect: org.hibernate.dialect.H2Dialect
        format_sql: true
        use_sql_comments: true
    open-in-view: false
```

### ddl-auto 选项

| 值 | 说明 |
|----|------|
| create | 每次启动时删除并重建表 |
| create-drop | 启动时创建，关闭时删除 |
| update | 只更新表结构（不删除） |
| validate | 只验证表结构，不修改 |
| none | 不做任何操作 |

**生产环境建议**：使用 `validate` 或 `none`，结合 Flyway/Liquibase 管理数据库变更。

## 常见问题

### 1. LazyInitializationException

**现象**：`org.hibernate.LazyInitializationException: could not initialize proxy - no Session`

**原因**：在 Session 关闭后访问懒加载属性。

**解决方案**：
- 使用 `@Transactional` 确保在事务内访问
- 使用 JOIN FETCH 一次性加载
- 设置 `open-in-view: true`（不推荐）

### 2. 循环引用导致 JSON 序列化失败

**现象**：`JsonMappingException: Infinite recursion (StackOverflow)`

**原因**：双向关系的循环引用。

**解决方案**：使用 `@JsonIgnore` 或 `@JsonManagedReference/@JsonBackReference`。

### 3. 双向关系数据不一致

**原因**：只维护了一端的关系。

**解决方案**：使用辅助方法同时维护两端关系。

## 学习资源

- [Hibernate 官方文档](https://hibernate.org/orm/documentation/5.6/)
- [Spring Data JPA 文档](https://docs.spring.io/spring-data/jpa/docs/current/reference/html/)
- [JPA 规范](https://jakarta.ee/specifications/persistence/)

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的核心概念
- ✅ 掌握相关的配置与命令
- ✅ 能够在本地环境中复现

## 🚀 快速开始

### 运行演示

```bash
./scripts/demo.sh
```

## 📖 核心概念

### 1. 基本概念

本节介绍本案例涉及的核心概念。

### 2. 适用场景

- 场景 1：学习与实验
- 场景 2：工程实践
- 场景 3：面试准备

## 💻 代码示例

### 基本用法

```bash
# 请根据实际案例替换
./scripts/demo.sh
```
