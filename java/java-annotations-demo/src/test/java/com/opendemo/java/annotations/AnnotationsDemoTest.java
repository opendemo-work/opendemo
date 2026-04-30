package com.opendemo.java.annotations;

import org.junit.jupiter.api.Test;
import java.util.List;
import static org.junit.jupiter.api.Assertions.*;

class AnnotationsDemoTest {

    @Test
    void testAuthorAnnotation() {
        AnnotationProcessor processor = new AnnotationProcessor();
        String authorInfo = processor.getAuthorInfo(CustomAnnotations.class);
        assertTrue(authorInfo.contains("OpenDemo"));
        assertTrue(authorInfo.contains("team@opendemo.com"));
    }

    @Test
    void testVersionAnnotation() {
        AnnotationProcessor processor = new AnnotationProcessor();
        String versionInfo = processor.getVersionInfo(CustomAnnotations.class);
        assertTrue(versionInfo.contains("1.0"));
        assertTrue(versionInfo.contains("2024-01-15"));
    }

    @Test
    void testClassAnnotations() {
        AnnotationProcessor processor = new AnnotationProcessor();
        List<String> annotations = processor.processClassAnnotations(CustomAnnotations.class);
        assertFalse(annotations.isEmpty());
        assertTrue(annotations.stream().anyMatch(a -> a.contains("Author")));
        assertTrue(annotations.stream().anyMatch(a -> a.contains("Version")));
    }

    @Test
    void testMethodAnnotations() {
        AnnotationProcessor processor = new AnnotationProcessor();
        List<String> annotations = processor.processMethodAnnotations(CustomAnnotations.class);
        assertFalse(annotations.isEmpty());
    }

    @Test
    void testGetTodos() {
        AnnotationProcessor processor = new AnnotationProcessor();
        List<String> todos = processor.getTodos(CustomAnnotations.class);
        assertFalse(todos.isEmpty());
        assertTrue(todos.stream().anyMatch(t -> t.contains("需要优化性能")));
        assertTrue(todos.stream().anyMatch(t -> t.contains("即将移除")));
    }

    @Test
    void testHasAnnotation() {
        AnnotationProcessor processor = new AnnotationProcessor();
        assertTrue(processor.hasAnnotation(CustomAnnotations.class, Author.class));
        assertTrue(processor.hasAnnotation(CustomAnnotations.class, Version.class));
        assertFalse(processor.hasAnnotation(CustomAnnotations.class, Deprecated.class));
    }

    @Test
    void testMethodHasAnnotation() {
        AnnotationProcessor processor = new AnnotationProcessor();
        assertTrue(processor.methodHasAnnotation(CustomAnnotations.class, "legacyMethod", Deprecated.class));
        assertTrue(processor.methodHasAnnotation(CustomAnnotations.class, "annotatedMethod", MyAnnotation.class));
        assertFalse(processor.methodHasAnnotation(CustomAnnotations.class, "toString", Author.class));
    }

    @Test
    void testMethodHasAnnotationNonExistent() {
        AnnotationProcessor processor = new AnnotationProcessor();
        assertFalse(processor.methodHasAnnotation(CustomAnnotations.class, "nonExistent", Deprecated.class));
    }

    @Test
    void testCustomAnnotationsMethods() {
        CustomAnnotations instance = new CustomAnnotations();
        assertEquals("HELLO", instance.annotatedMethod("hello"));
        assertEquals("legacy", instance.legacyMethod());
        assertEquals("CustomAnnotations instance", instance.toString());
    }

    @Test
    void testRunAll() {
        AnnotationsDemo demo = new AnnotationsDemo();
        assertDoesNotThrow(() -> demo.runAll());
    }
}
