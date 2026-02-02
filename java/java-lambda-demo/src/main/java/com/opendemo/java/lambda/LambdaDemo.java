package com.opendemo.java.lambda;

import java.util.function.Function;

public class LambdaDemo {
    public static void main(String[] args) {
        // Lambda表达式示例
        Function<String, Integer> stringLength = str -> str.length();
        System.out.println("字符串长度: " + stringLength.apply("Hello"));
        
        // 方法引用示例
        Function<String, String> upperCase = String::toUpperCase;
        System.out.println("大写转换: " + upperCase.apply("hello"));
    }
}