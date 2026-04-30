package com.example.demo.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.expression.Expression;
import org.springframework.expression.ExpressionParser;
import org.springframework.expression.spel.standard.SpelExpressionParser;
import org.springframework.expression.spel.support.StandardEvaluationContext;
import org.springframework.stereotype.Service;

import com.example.demo.model.User;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class SpelService {

    private static final Logger logger = LoggerFactory.getLogger(SpelService.class);
    private final ExpressionParser parser = new SpelExpressionParser();

    public Object evaluateLiteral(String expression) {
        Expression exp = parser.parseExpression(expression);
        return exp.getValue();
    }

    public Object evaluateWithContext(String expression, Object rootObject) {
        StandardEvaluationContext context = new StandardEvaluationContext(rootObject);
        Expression exp = parser.parseExpression(expression);
        return exp.getValue(context);
    }

    public Object evaluateWithVariables(String expression, Map<String, Object> variables) {
        StandardEvaluationContext context = new StandardEvaluationContext();
        variables.forEach(context::setVariable);
        Expression exp = parser.parseExpression(expression);
        return exp.getValue(context);
    }

    public List<String> demonstrateBasicExpressions() {
        List<String> results = new ArrayList<>();

        results.add("1 + 2 = " + parser.parseExpression("1 + 2").getValue());
        results.add("2 * 3 = " + parser.parseExpression("2 * 3").getValue());
        results.add("'Hello' + ' ' + 'World' = " + parser.parseExpression("'Hello' + ' ' + 'World'").getValue());
        results.add("true AND false = " + parser.parseExpression("true and false").getValue());
        results.add("10 > 5 = " + parser.parseExpression("10 > 5").getValue());
        results.add("T(Math).random() = " + parser.parseExpression("T(java.lang.Math).random()").getValue());
        results.add("'hello'.toUpperCase() = " + parser.parseExpression("'hello'.toUpperCase()").getValue());

        return results;
    }

    public Map<String, Object> demonstrateUserExpressions(User user) {
        Map<String, Object> results = new HashMap<>();
        StandardEvaluationContext context = new StandardEvaluationContext(user);

        results.put("name", parser.parseExpression("name").getValue(context));
        results.put("age", parser.parseExpression("age").getValue(context));
        results.put("active", parser.parseExpression("active").getValue(context));
        results.put("isAdmin", parser.parseExpression("isAdmin()").getValue(context));
        results.put("displayName", parser.parseExpression("getDisplayName()").getValue(context));
        results.put("age > 18", parser.parseExpression("age > 18").getValue(context));
        results.put("active AND isAdmin()", parser.parseExpression("active and isAdmin()").getValue(context));

        return results;
    }

    public List<String> demonstrateCollectionExpressions() {
        List<String> results = new ArrayList<>();

        List<Integer> numbers = List.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
        StandardEvaluationContext context = new StandardEvaluationContext();
        context.setVariable("numbers", numbers);

        results.add("过滤偶数: " + parser.parseExpression("#numbers.?[#this % 2 == 0]").getValue(context));
        results.add("第一个>5: " + parser.parseExpression("#numbers.^[#this > 5]").getValue(context));
        results.add("最后一个: " + parser.parseExpression("#numbers.$[#this > 8]").getValue(context));
        results.add("投影*2: " + parser.parseExpression("#numbers.![#this * 2]").getValue(context));
        results.add("包含5: " + parser.parseExpression("#numbers.contains(5)").getValue(context));

        return results;
    }

    public Object demonstrateTernary(boolean condition, String trueValue, String falseValue) {
        String expression = condition ? "'" + trueValue + "'" : "'" + falseValue + "'";
        return parser.parseExpression(condition ? "'" + trueValue + "'" : "'" + falseValue + "'").getValue();
    }

    public String demonstrateElvis(User user) {
        StandardEvaluationContext context = new StandardEvaluationContext(user);
        return parser.parseExpression("name ?: 'Unknown'").getValue(context, String.class);
    }

    public String demonstrateSafeNavigation(User user) {
        StandardEvaluationContext context = new StandardEvaluationContext(user);
        return parser.parseExpression("name?.length()").getValue(context, String.class);
    }
}
