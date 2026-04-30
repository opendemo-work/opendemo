package com.opendemo.java.annotations;

import java.lang.annotation.*;

@Retention(RetentionPolicy.RUNTIME)
@Target({ElementType.TYPE, ElementType.METHOD})
public @interface Author {
    String name() default "Unknown";
    String email() default "";
}
