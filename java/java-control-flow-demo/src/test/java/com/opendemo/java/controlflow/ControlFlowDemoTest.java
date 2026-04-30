package com.opendemo.java.controlflow;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.ArrayList;
import java.util.List;

class ControlFlowDemoTest {

    @Test
    void testIfElseCondition() {
        int score = 85;
        String grade;
        if (score >= 90) {
            grade = "A";
        } else if (score >= 80) {
            grade = "B";
        } else if (score >= 70) {
            grade = "C";
        } else if (score >= 60) {
            grade = "D";
        } else {
            grade = "F";
        }
        assertEquals("B", grade);
    }

    @Test
    void testSwitchStatement() {
        int dayOfWeek = 3;
        String dayName;
        switch (dayOfWeek) {
            case 1: dayName = "星期一"; break;
            case 2: dayName = "星期二"; break;
            case 3: dayName = "星期三"; break;
            case 4: dayName = "星期四"; break;
            case 5: dayName = "星期五"; break;
            case 6: dayName = "星期六"; break;
            case 7: dayName = "星期日"; break;
            default: dayName = "无效";
        }
        assertEquals("星期三", dayName);
    }

    @Test
    void testTernaryOperator() {
        int score = 85;
        String result = score >= 60 ? "通过" : "未通过";
        assertEquals("通过", result);

        score = 45;
        result = score >= 60 ? "通过" : "未通过";
        assertEquals("未通过", result);
    }

    @Test
    void testForLoop() {
        int sum = 0;
        for (int i = 1; i <= 10; i++) {
            sum += i;
        }
        assertEquals(55, sum);
    }

    @Test
    void testWhileLoop() {
        int countdown = 5;
        int iterations = 0;
        while (countdown > 0) {
            countdown--;
            iterations++;
        }
        assertEquals(5, iterations);
        assertEquals(0, countdown);
    }

    @Test
    void testDoWhileLoop() {
        int count = 0;
        int iterations = 0;
        do {
            count++;
            iterations++;
        } while (count < 3);
        assertEquals(3, iterations);
        assertEquals(3, count);
    }

    @Test
    void testDoWhileLoopExecutesAtLeastOnce() {
        int count = 10;
        int iterations = 0;
        do {
            iterations++;
        } while (count < 5);
        assertEquals(1, iterations);
    }

    @Test
    void testForEachLoop() {
        String[] colors = {"红色", "绿色", "蓝色", "黄色"};
        List<String> collected = new ArrayList<>();
        for (String color : colors) {
            collected.add(color);
        }
        assertEquals(4, collected.size());
        assertEquals("红色", collected.get(0));
        assertEquals("黄色", collected.get(3));
    }

    @Test
    void testBreakStatement() {
        int[] numbers = {1, 3, 5, 8, 9, 12, 15};
        int firstEven = -1;
        for (int num : numbers) {
            if (num % 2 == 0) {
                firstEven = num;
                break;
            }
        }
        assertEquals(8, firstEven);
    }

    @Test
    void testContinueStatement() {
        List<Integer> evens = new ArrayList<>();
        for (int i = 1; i <= 10; i++) {
            if (i % 2 != 0) {
                continue;
            }
            evens.add(i);
        }
        assertEquals(List.of(2, 4, 6, 8, 10), evens);
    }

    @Test
    void testLabeledBreak() {
        int foundI = -1;
        int foundJ = -1;
        outerLoop:
        for (int i = 1; i <= 3; i++) {
            for (int j = 1; j <= 3; j++) {
                if (i == 2 && j == 2) {
                    foundI = i;
                    foundJ = j;
                    break outerLoop;
                }
            }
        }
        assertEquals(2, foundI);
        assertEquals(2, foundJ);
    }

    @Test
    void testNestedConditionals() {
        int age = 25;
        boolean hasLicense = true;
        boolean hasCar = false;

        String message;
        if (age >= 18) {
            if (hasLicense) {
                if (hasCar) {
                    message = "可以开车出行";
                } else {
                    message = "需要购买车辆";
                }
            } else {
                message = "需要考取驾照";
            }
        } else {
            message = "未成年，不能开车";
        }
        assertEquals("需要购买车辆", message);
    }

    @Test
    void testPrimeNumberCheck() {
        assertTrue(isPrime(2));
        assertTrue(isPrime(3));
        assertTrue(isPrime(5));
        assertTrue(isPrime(7));
        assertTrue(isPrime(11));
        assertTrue(isPrime(13));
        assertFalse(isPrime(4));
        assertFalse(isPrime(6));
        assertFalse(isPrime(9));
        assertFalse(isPrime(15));
    }

    private boolean isPrime(int num) {
        if (num < 2) return false;
        for (int i = 2; i <= Math.sqrt(num); i++) {
            if (num % i == 0) return false;
        }
        return true;
    }

    @Test
    void testEmailValidation() {
        assertTrue(isValidEmail("user@example.com"));
        assertTrue(isValidEmail("admin@test.org"));
        assertFalse(isValidEmail("invalid-email"));
        assertFalse(isValidEmail("missingatsign.com"));
    }

    private boolean isValidEmail(String email) {
        return email.contains("@") && email.contains(".");
    }

    @Test
    void testScoreAnalysis() {
        int[] scores = {85, 92, 78, 96, 88, 73, 91, 84};
        int sum = 0;
        int max = scores[0];
        int min = scores[0];

        for (int score : scores) {
            sum += score;
            if (score > max) max = score;
            if (score < min) min = score;
        }

        double average = (double) sum / scores.length;
        assertEquals(85.875, average, 0.001);
        assertEquals(96, max);
        assertEquals(73, min);
    }

    @Test
    void testMultiplicationTable() {
        int[][] table = new int[9][9];
        for (int i = 1; i <= 9; i++) {
            for (int j = 1; j <= i; j++) {
                table[i - 1][j - 1] = i * j;
            }
        }
        assertEquals(1, table[0][0]);
        assertEquals(6, table[2][2]);
        assertEquals(81, table[8][8]);
    }
}
