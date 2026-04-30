package com.opendemo.java.annotations;

import java.lang.annotation.*;

@Retention(RetentionPolicy.RUNTIME)
@Target({ElementType.METHOD, ElementType.CONSTRUCTOR})
public @interface Todo {
    String value();
    String assignee() default "";
    TodoPriority priority() default TodoPriority.MEDIUM;
}
