package com.example.demo;

import com.example.demo.service.SpelService;
import com.example.demo.model.User;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.expression.ExpressionParser;
import org.springframework.expression.spel.standard.SpelExpressionParser;
import org.springframework.expression.spel.support.StandardEvaluationContext;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

class SpelDemoTest {

    private ExpressionParser parser;
    private SpelService spelService;

    @BeforeEach
    void setUp() {
        parser = new SpelExpressionParser();
        spelService = new SpelService();
    }

    @Test
    void testLiteralExpression() {
        assertEquals("Hello World", parser.parseExpression("'Hello World'").getValue());
        assertEquals(42, parser.parseExpression("42").getValue());
        assertEquals(true, parser.parseExpression("true").getValue());
    }

    @Test
    void testArithmeticExpressions() {
        assertEquals(3, parser.parseExpression("1 + 2").getValue());
        assertEquals(6, parser.parseExpression("2 * 3").getValue());
        assertEquals(1, parser.parseExpression("7 % 2").getValue());
    }

    @Test
    void testStringConcatenation() {
        assertEquals("Hello World", parser.parseExpression("'Hello' + ' ' + 'World'").getValue());
    }

    @Test
    void testComparisonExpressions() {
        assertEquals(true, parser.parseExpression("10 > 5").getValue());
        assertEquals(false, parser.parseExpression("3 == 5").getValue());
        assertEquals(true, parser.parseExpression("10 >= 10").getValue());
    }

    @Test
    void testLogicalExpressions() {
        assertEquals(true, parser.parseExpression("true and true").getValue());
        assertEquals(false, parser.parseExpression("true and false").getValue());
        assertEquals(true, parser.parseExpression("true or false").getValue());
        assertEquals(false, parser.parseExpression("!true").getValue());
    }

    @Test
    void testPropertyAccess() {
        User user = new User(1L, "张三", 25, "ADMIN", true);
        StandardEvaluationContext context = new StandardEvaluationContext(user);

        assertEquals("张三", parser.parseExpression("name").getValue(context));
        assertEquals(25, parser.parseExpression("age").getValue(context));
        assertEquals(true, parser.parseExpression("active").getValue(context));
    }

    @Test
    void testMethodInvocation() {
        User user = new User(1L, "张三", 25, "ADMIN", true);
        StandardEvaluationContext context = new StandardEvaluationContext(user);

        assertEquals(true, parser.parseExpression("isAdmin()").getValue(context));
        assertEquals("张三 (ADMIN)", parser.parseExpression("getDisplayName()").getValue(context));
    }

    @Test
    void testUserNotAdmin() {
        User user = new User(2L, "李四", 30, "USER", true);
        StandardEvaluationContext context = new StandardEvaluationContext(user);

        assertEquals(false, parser.parseExpression("isAdmin()").getValue(context));
    }

    @Test
    void testStaticMethod() {
        Object result = parser.parseExpression("T(java.lang.Math).random()").getValue();
        assertNotNull(result);
        assertTrue((Double) result >= 0.0 && (Double) result < 1.0);
    }

    @Test
    void testCollectionFilter() {
        List<Integer> numbers = List.of(1, 2, 3, 4, 5);
        StandardEvaluationContext context = new StandardEvaluationContext();
        context.setVariable("numbers", numbers);

        @SuppressWarnings("unchecked")
        List<Integer> evens = (List<Integer>) parser.parseExpression("#numbers.?[#this % 2 == 0]").getValue(context);
        assertEquals(List.of(2, 4), evens);
    }

    @Test
    void testCollectionProjection() {
        List<Integer> numbers = List.of(1, 2, 3);
        StandardEvaluationContext context = new StandardEvaluationContext();
        context.setVariable("numbers", numbers);

        @SuppressWarnings("unchecked")
        List<Integer> doubled = (List<Integer>) parser.parseExpression("#numbers.![#this * 2]").getValue(context);
        assertEquals(List.of(2, 4, 6), doubled);
    }

    @Test
    void testVariables() {
        Map<String, Object> variables = new HashMap<>();
        variables.put("name", "张三");
        variables.put("age", 25);

        Object result = spelService.evaluateWithVariables("#name + ' is ' + #age", variables);
        assertEquals("张三 is 25", result);
    }

    @Test
    void testSpelServiceBasicExpressions() {
        List<String> results = spelService.demonstrateBasicExpressions();
        assertFalse(results.isEmpty());
    }

    @Test
    void testSpelServiceUserExpressions() {
        User user = new User(1L, "张三", 25, "ADMIN", true);
        Map<String, Object> results = spelService.demonstrateUserExpressions(user);
        assertEquals("张三", results.get("name"));
        assertEquals(25, results.get("age"));
        assertEquals(true, results.get("isAdmin"));
    }

    @Test
    void testSpelServiceCollectionExpressions() {
        List<String> results = spelService.demonstrateCollectionExpressions();
        assertFalse(results.isEmpty());
    }

    @Test
    void testUserModel() {
        User user = new User(1L, "张三", 25, "ADMIN", true);
        assertEquals(1L, user.getId());
        assertEquals("张三", user.getName());
        assertEquals(25, user.getAge());
        assertEquals("ADMIN", user.getRole());
        assertTrue(user.isActive());
        assertTrue(user.isAdmin());
    }

    @Test
    void testUserModelSetters() {
        User user = new User();
        user.setId(2L);
        user.setName("李四");
        user.setAge(30);
        user.setRole("USER");
        user.setActive(false);
        assertEquals("李四", user.getName());
        assertFalse(user.isActive());
        assertFalse(user.isAdmin());
    }
}
