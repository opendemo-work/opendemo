package com.opendemo.java.reflection;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.lang.reflect.*;
import java.util.ArrayList;
import java.util.List;

public class ReflectionUtils {
    private static final Logger logger = LoggerFactory.getLogger(ReflectionUtils.class);

    public static List<String> getClassInfo(Class<?> clazz) {
        List<String> info = new ArrayList<>();
        info.add("类名: " + clazz.getName());
        info.add("简单类名: " + clazz.getSimpleName());
        info.add("包名: " + clazz.getPackage().getName());
        info.add("修饰符: " + Modifier.toString(clazz.getModifiers()));
        info.add("父类: " + clazz.getSuperclass().getName());
        for (Class<?> iface : clazz.getInterfaces()) {
            info.add("实现接口: " + iface.getName());
        }
        return info;
    }

    public static List<String> getFields(Class<?> clazz) {
        List<String> fields = new ArrayList<>();
        for (Field field : clazz.getDeclaredFields()) {
            String fieldInfo = Modifier.toString(field.getModifiers()) + " "
                    + field.getType().getSimpleName() + " "
                    + field.getName();
            fields.add(fieldInfo);
            logger.info("字段: {}", fieldInfo);
        }
        return fields;
    }

    public static List<String> getMethods(Class<?> clazz) {
        List<String> methods = new ArrayList<>();
        for (Method method : clazz.getDeclaredMethods()) {
            String methodInfo = Modifier.toString(method.getModifiers()) + " "
                    + method.getReturnType().getSimpleName() + " "
                    + method.getName()
                    + "(" + getParameterTypes(method) + ")";
            methods.add(methodInfo);
            logger.info("方法: {}", methodInfo);
        }
        return methods;
    }

    private static String getParameterTypes(Method method) {
        StringBuilder sb = new StringBuilder();
        Class<?>[] params = method.getParameterTypes();
        for (int i = 0; i < params.length; i++) {
            if (i > 0) sb.append(", ");
            sb.append(params[i].getSimpleName());
        }
        return sb.toString();
    }

    public static List<String> getConstructors(Class<?> clazz) {
        List<String> constructors = new ArrayList<>();
        for (Constructor<?> constructor : clazz.getDeclaredConstructors()) {
            String constructorInfo = Modifier.toString(constructor.getModifiers()) + " "
                    + constructor.getName()
                    + "(" + getConstructorParameterTypes(constructor) + ")";
            constructors.add(constructorInfo);
            logger.info("构造器: {}", constructorInfo);
        }
        return constructors;
    }

    private static String getConstructorParameterTypes(Constructor<?> constructor) {
        StringBuilder sb = new StringBuilder();
        Class<?>[] params = constructor.getParameterTypes();
        for (int i = 0; i < params.length; i++) {
            if (i > 0) sb.append(", ");
            sb.append(params[i].getSimpleName());
        }
        return sb.toString();
    }

    public static Object getFieldValue(Object obj, String fieldName) throws Exception {
        Field field = obj.getClass().getDeclaredField(fieldName);
        field.setAccessible(true);
        return field.get(obj);
    }

    public static void setFieldValue(Object obj, String fieldName, Object value) throws Exception {
        Field field = obj.getClass().getDeclaredField(fieldName);
        field.setAccessible(true);
        field.set(obj, value);
    }

    public static Object invokeMethod(Object obj, String methodName, Class<?>[] paramTypes, Object[] args) throws Exception {
        Method method = obj.getClass().getDeclaredMethod(methodName, paramTypes);
        method.setAccessible(true);
        return method.invoke(obj, args);
    }

    public static Object createInstance(Class<?> clazz, Class<?>[] paramTypes, Object[] args) throws Exception {
        Constructor<?> constructor = clazz.getDeclaredConstructor(paramTypes);
        constructor.setAccessible(true);
        return constructor.newInstance(args);
    }
}
