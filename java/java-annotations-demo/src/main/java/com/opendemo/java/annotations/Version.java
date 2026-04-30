package com.opendemo.java.annotations;

import java.lang.annotation.*;

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
public @interface Version {
    int major() default 1;
    int minor() default 0;
    String date() default "";
}
