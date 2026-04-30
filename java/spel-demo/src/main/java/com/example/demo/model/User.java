package com.example.demo.model;

public class User {

    private Long id;
    private String name;
    private int age;
    private String role;
    private boolean active;

    public User() {}

    public User(Long id, String name, int age, String role, boolean active) {
        this.id = id;
        this.name = name;
        this.age = age;
        this.role = role;
        this.active = active;
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public int getAge() { return age; }
    public void setAge(int age) { this.age = age; }
    public String getRole() { return role; }
    public void setRole(String role) { this.role = role; }
    public boolean isActive() { return active; }
    public void setActive(boolean active) { this.active = active; }

    public boolean isAdmin() {
        return "ADMIN".equals(role);
    }

    public String getDisplayName() {
        return name + " (" + role + ")";
    }

    @Override
    public String toString() {
        return "User{id=" + id + ", name='" + name + "', age=" + age + ", role='" + role + "', active=" + active + "}";
    }
}
