package com.opendemo.java.reflection;

import org.junit.jupiter.api.Test;
import java.util.List;
import static org.junit.jupiter.api.Assertions.*;

class ReflectionDemoTest {

    @Test
    void testGetClassInfo() {
        List<String> info = ReflectionUtils.getClassInfo(SampleClass.class);
        assertFalse(info.isEmpty());
        assertTrue(info.stream().anyMatch(i -> i.contains("SampleClass")));
        assertTrue(info.stream().anyMatch(i -> i.contains("com.opendemo.java.reflection")));
    }

    @Test
    void testGetFields() {
        List<String> fields = ReflectionUtils.getFields(SampleClass.class);
        assertFalse(fields.isEmpty());
        assertTrue(fields.stream().anyMatch(f -> f.contains("name")));
        assertTrue(fields.stream().anyMatch(f -> f.contains("age")));
    }

    @Test
    void testGetMethods() {
        List<String> methods = ReflectionUtils.getMethods(SampleClass.class);
        assertFalse(methods.isEmpty());
        assertTrue(methods.stream().anyMatch(m -> m.contains("getName")));
        assertTrue(methods.stream().anyMatch(m -> m.contains("greet")));
    }

    @Test
    void testGetConstructors() {
        List<String> constructors = ReflectionUtils.getConstructors(SampleClass.class);
        assertFalse(constructors.isEmpty());
        assertTrue(constructors.size() >= 3);
    }

    @Test
    void testGetFieldValue() throws Exception {
        SampleClass sample = new SampleClass("test", 25);
        assertEquals("test", ReflectionUtils.getFieldValue(sample, "name"));
        assertEquals(25, ReflectionUtils.getFieldValue(sample, "age"));
    }

    @Test
    void testSetFieldValue() throws Exception {
        SampleClass sample = new SampleClass("old", 20);
        ReflectionUtils.setFieldValue(sample, "name", "new");
        ReflectionUtils.setFieldValue(sample, "age", 30);
        assertEquals("new", sample.getName());
        assertEquals(30, sample.getAge());
    }

    @Test
    void testInvokePublicMethod() throws Exception {
        SampleClass sample = new SampleClass("张三", 25);
        String result = (String) ReflectionUtils.invokeMethod(
                sample, "greet", new Class[]{String.class}, new Object[]{"Hello"});
        assertEquals("Hello, I am 张三", result);
    }

    @Test
    void testInvokePrivateMethod() throws Exception {
        SampleClass sample = new SampleClass("test", 20);
        String result = (String) ReflectionUtils.invokeMethod(
                sample, "privateMethod", new Class[]{String.class}, new Object[]{"input"});
        assertEquals("processed: input", result);
    }

    @Test
    void testInvokeStaticMethod() throws Exception {
        String result = (String) ReflectionUtils.invokeMethod(
                null, "staticMethod", new Class[]{}, new Object[]{});
        assertEquals("static result", result);
    }

    @Test
    void testCreateInstanceNoArgs() throws Exception {
        Object instance = ReflectionUtils.createInstance(SampleClass.class, new Class[]{}, new Object[]{});
        assertNotNull(instance);
        assertTrue(instance instanceof SampleClass);
        assertEquals("default", ((SampleClass) instance).getName());
    }

    @Test
    void testCreateInstanceWithArgs() throws Exception {
        Object instance = ReflectionUtils.createInstance(
                SampleClass.class, new Class[]{String.class, int.class}, new Object[]{"test", 42});
        assertNotNull(instance);
        assertEquals("test", ((SampleClass) instance).getName());
        assertEquals(42, ((SampleClass) instance).getAge());
    }

    @Test
    void testCreateInstancePrivateConstructor() throws Exception {
        Object instance = ReflectionUtils.createInstance(
                SampleClass.class, new Class[]{String.class}, new Object[]{"private"});
        assertNotNull(instance);
        assertEquals("private", ((SampleClass) instance).getName());
    }

    @Test
    void testRunAll() {
        ReflectionDemo demo = new ReflectionDemo();
        assertDoesNotThrow(() -> demo.runAll());
    }
}
