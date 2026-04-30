package com.opendemo.java.annotations;

@Author(name = "OpenDemo", email = "team@opendemo.com")
@Version(major = 1, minor = 0, date = "2024-01-15")
public class CustomAnnotations {

    @MyAnnotation(value = "示例方法", count = 3)
    public String annotatedMethod(String input) {
        return input.toUpperCase();
    }

    @Todo(value = "需要优化性能", assignee = "developer", priority = TodoPriority.HIGH)
    public void pendingMethod() {
    }

    @Deprecated
    @Todo(value = "即将移除", priority = TodoPriority.LOW)
    public String legacyMethod() {
        return "legacy";
    }

    @Override
    public String toString() {
        return "CustomAnnotations instance";
    }
}
