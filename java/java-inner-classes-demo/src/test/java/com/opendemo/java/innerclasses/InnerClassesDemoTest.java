package com.opendemo.java.innerclasses;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class InnerClassesDemoTest {

    @Test
    void testMemberInnerClass() {
        OuterClass outer = new OuterClass();
        OuterClass.InnerClass inner = outer.createInner();
        assertNotNull(inner);
        assertEquals("外部类字段 + 成员内部类字段", inner.getOuterField() + " + " + inner.getInnerField());
    }

    @Test
    void testStaticNestedClass() {
        OuterClass.StaticNestedClass nested = new OuterClass.StaticNestedClass();
        assertNotNull(nested);
        assertEquals("静态嵌套类字段", nested.getNestedField());
    }

    @Test
    void testLocalClass() {
        OuterClass outer = new OuterClass();
        String result = outer.demonstrateLocalClass("PREFIX");
        assertTrue(result.contains("PREFIX"));
        assertTrue(result.contains("局部内部类处理结果"));
        assertTrue(result.contains("局部内部类字段"));
    }

    @Test
    void testAnonymousClass() {
        InnerClassesDemo demo = new InnerClassesDemo();
        String result = demo.demonstrateAnonymousClass();
        assertEquals("匿名内部类执行完成", result);
    }

    @Test
    void testAnonymousInterface() {
        InnerClassesDemo demo = new InnerClassesDemo();
        String result = demo.demonstrateAnonymousInterface();
        assertEquals("HELLO", result);
    }

    @Test
    void testRunAll() {
        InnerClassesDemo demo = new InnerClassesDemo();
        assertDoesNotThrow(() -> demo.runAll());
    }

    @Test
    void testMemberInnerClassAccessOuter() {
        OuterClass outer = new OuterClass();
        OuterClass.InnerClass inner = outer.new InnerClass();
        assertEquals("外部类字段", inner.getOuterField());
    }

    @Test
    void testMultipleInnerInstances() {
        OuterClass outer = new OuterClass();
        OuterClass.InnerClass inner1 = outer.createInner();
        OuterClass.InnerClass inner2 = outer.createInner();
        assertNotSame(inner1, inner2);
        assertEquals(inner1.getOuterField(), inner2.getOuterField());
    }
}
