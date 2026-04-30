package com.opendemo.java.annotations;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.lang.annotation.Annotation;
import java.lang.reflect.AnnotatedElement;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.List;

public class AnnotationProcessor {
    private static final Logger logger = LoggerFactory.getLogger(AnnotationProcessor.class);

    public List<String> processClassAnnotations(Class<?> clazz) {
        List<String> results = new ArrayList<>();
        Annotation[] annotations = clazz.getAnnotations();
        for (Annotation annotation : annotations) {
            results.add(annotation.annotationType().getSimpleName() + ": " + annotation.toString());
            logger.info("类注解: {}", annotation);
        }
        return results;
    }

    public List<String> processMethodAnnotations(Class<?> clazz) {
        List<String> results = new ArrayList<>();
        Method[] methods = clazz.getDeclaredMethods();
        for (Method method : methods) {
            Annotation[] methodAnnotations = method.getAnnotations();
            for (Annotation annotation : methodAnnotations) {
                String entry = method.getName() + " -> " + annotation.annotationType().getSimpleName();
                results.add(entry);
                logger.info("方法注解: {}", entry);
            }
        }
        return results;
    }

    public String getAuthorInfo(Class<?> clazz) {
        Author author = clazz.getAnnotation(Author.class);
        if (author != null) {
            return author.name() + " <" + author.email() + ">";
        }
        return "No author info";
    }

    public String getVersionInfo(Class<?> clazz) {
        Version version = clazz.getAnnotation(Version.class);
        if (version != null) {
            return version.major() + "." + version.minor() + " (" + version.date() + ")";
        }
        return "No version info";
    }

    public List<String> getTodos(Class<?> clazz) {
        List<String> todos = new ArrayList<>();
        Method[] methods = clazz.getDeclaredMethods();
        for (Method method : methods) {
            Todo todo = method.getAnnotation(Todo.class);
            if (todo != null) {
                todos.add(method.getName() + ": " + todo.value() + " [" + todo.priority() + "]");
            }
        }
        return todos;
    }

    public boolean hasAnnotation(Class<?> clazz, Class<? extends Annotation> annotationClass) {
        return clazz.isAnnotationPresent(annotationClass);
    }

    public boolean methodHasAnnotation(Class<?> clazz, String methodName, Class<? extends Annotation> annotationClass) {
        try {
            Method method = clazz.getDeclaredMethod(methodName);
            return method.isAnnotationPresent(annotationClass);
        } catch (NoSuchMethodException e) {
            return false;
        }
    }
}
