package com.example;

/**
 * Java控制流程语句演示程序
 * 展示条件语句、循环语句和跳转语句的各种用法
 * 
 * @author OpenDemo Team
 * @version 1.0.0
 */
public class ControlFlowDemo {
    
    public static void main(String[] args) {
        System.out.println("=== Java控制流程语句演示 ===\n");
        
        // 1. 条件语句演示
        demonstrateConditionalStatements();
        
        // 2. 循环语句演示
        demonstrateLoopStatements();
        
        // 3. 跳转语句演示
        demonstrateJumpStatements();
        
        // 4. 嵌套控制结构演示
        demonstrateNestedStructures();
        
        // 5. 实际应用场景演示
        demonstratePracticalApplications();
    }
    
    /**
     * 演示条件语句
     */
    private static void demonstrateConditionalStatements() {
        System.out.println("1. 条件语句演示:");
        
        int score = 85;
        
        // if-else语句
        if (score >= 90) {
            System.out.println("成绩等级: 优秀 (A)");
        } else if (score >= 80) {
            System.out.println("成绩等级: 良好 (B)");
        } else if (score >= 70) {
            System.out.println("成绩等级: 中等 (C)");
        } else if (score >= 60) {
            System.out.println("成绩等级: 及格 (D)");
        } else {
            System.out.println("成绩等级: 不及格 (F)");
        }
        
        // 三元运算符
        String result = score >= 60 ? "通过" : "未通过";
        System.out.println("考试结果: " + result);
        
        // switch语句 (传统写法)
        int dayOfWeek = 3;
        switch (dayOfWeek) {
            case 1:
                System.out.println("今天是星期一");
                break;
            case 2:
                System.out.println("今天是星期二");
                break;
            case 3:
                System.out.println("今天是星期三");
                break;
            case 4:
                System.out.println("今天是星期四");
                break;
            case 5:
                System.out.println("今天是星期五");
                break;
            case 6:
                System.out.println("今天是星期六");
                break;
            case 7:
                System.out.println("今天是星期日");
                break;
            default:
                System.out.println("无效的星期数");
        }
        
        // switch表达式 (Java 14+)
        String dayName = switch (dayOfWeek) {
            case 1 -> "星期一";
            case 2 -> "星期二";
            case 3 -> "星期三";
            case 4 -> "星期四";
            case 5 -> "星期五";
            case 6 -> "星期六";
            case 7 -> "星期日";
            default -> "无效日期";
        };
        System.out.println("Switch表达式结果: " + dayName);
        
        System.out.println();
    }
    
    /**
     * 演示循环语句
     */
    private static void demonstrateLoopStatements() {
        System.out.println("2. 循环语句演示:");
        
        // for循环 - 计数循环
        System.out.println("for循环 - 输出1到10:");
        for (int i = 1; i <= 10; i++) {
            System.out.print(i + " ");
        }
        System.out.println();
        
        // while循环 - 条件循环
        System.out.println("\nwhile循环 - 倒计时:");
        int countdown = 5;
        while (countdown > 0) {
            System.out.println("倒计时: " + countdown);
            countdown--;
        }
        System.out.println("发射!");
        
        // do-while循环 - 至少执行一次
        System.out.println("\ndo-while循环 - 用户输入模拟:");
        int userInput = 0;
        do {
            System.out.println("请输入数字(输入0退出): " + userInput);
            userInput++;
        } while (userInput < 3);
        
        // 增强for循环 (for-each)
        System.out.println("\n增强for循环 - 遍历数组:");
        String[] colors = {"红色", "绿色", "蓝色", "黄色"};
        for (String color : colors) {
            System.out.println("颜色: " + color);
        }
        
        // 嵌套for循环
        System.out.println("\n嵌套for循环 - 九九乘法表:");
        for (int i = 1; i <= 9; i++) {
            for (int j = 1; j <= i; j++) {
                System.out.print(j + "×" + i + "=" + (i * j) + "\t");
            }
            System.out.println();
        }
        
        System.out.println();
    }
    
    /**
     * 演示跳转语句
     */
    private static void demonstrateJumpStatements() {
        System.out.println("3. 跳转语句演示:");
        
        // break语句 - 跳出循环
        System.out.println("break语句 - 寻找第一个偶数:");
        int[] numbers = {1, 3, 5, 8, 9, 12, 15};
        for (int num : numbers) {
            if (num % 2 == 0) {
                System.out.println("找到第一个偶数: " + num);
                break; // 跳出循环
            }
            System.out.println("检查数字: " + num);
        }
        
        // continue语句 - 跳过当前迭代
        System.out.println("\ncontinue语句 - 跳过奇数:");
        for (int i = 1; i <= 10; i++) {
            if (i % 2 != 0) {
                continue; // 跳过奇数
            }
            System.out.println("偶数: " + i);
        }
        
        // 带标签的break和continue
        System.out.println("\n带标签的break - 退出外层循环:");
        outerLoop: for (int i = 1; i <= 3; i++) {
            for (int j = 1; j <= 3; j++) {
                if (i == 2 && j == 2) {
                    System.out.println("在(" + i + "," + j + ")处跳出外层循环");
                    break outerLoop; // 跳出外层循环
                }
                System.out.println("位置: (" + i + "," + j + ")");
            }
        }
        
        System.out.println();
    }
    
    /**
     * 演示嵌套控制结构
     */
    private static void demonstrateNestedStructures() {
        System.out.println("4. 嵌套控制结构演示:");
        
        // 复杂的条件嵌套
        int age = 25;
        boolean hasLicense = true;
        boolean hasCar = false;
        
        if (age >= 18) {
            System.out.println("已成年");
            if (hasLicense) {
                System.out.println("有驾照");
                if (hasCar) {
                    System.out.println("可以开车出行");
                } else {
                    System.out.println("需要购买车辆");
                }
            } else {
                System.out.println("需要考取驾照");
            }
        } else {
            System.out.println("未成年，不能开车");
        }
        
        // 循环中的条件判断
        System.out.println("\n循环中的条件判断 - 筛选质数:");
        for (int num = 2; num <= 20; num++) {
            boolean isPrime = true;
            for (int i = 2; i <= Math.sqrt(num); i++) {
                if (num % i == 0) {
                    isPrime = false;
                    break;
                }
            }
            if (isPrime) {
                System.out.print(num + " ");
            }
        }
        System.out.println();
        
        System.out.println();
    }
    
    /**
     * 演示实际应用场景
     */
    private static void demonstratePracticalApplications() {
        System.out.println("5. 实际应用场景演示:");
        
        // 用户菜单系统
        System.out.println("简单菜单系统模拟:");
        int choice = 2; // 模拟用户选择
        
        switch (choice) {
            case 1:
                System.out.println("执行新建操作");
                createNewFile();
                break;
            case 2:
                System.out.println("执行打开操作");
                openExistingFile();
                break;
            case 3:
                System.out.println("执行保存操作");
                saveCurrentFile();
                break;
            case 4:
                System.out.println("退出程序");
                System.exit(0);
            default:
                System.out.println("无效选项");
        }
        
        // 数据验证示例
        System.out.println("\n数据验证示例:");
        String[] emails = {"user@example.com", "invalid-email", "admin@test.org"};
        for (String email : emails) {
            if (isValidEmail(email)) {
                System.out.println(email + " 是有效的邮箱地址");
            } else {
                System.out.println(email + " 是无效的邮箱地址");
            }
        }
        
        // 统计分析示例
        System.out.println("\n统计分析示例:");
        int[] scores = {85, 92, 78, 96, 88, 73, 91, 84};
        analyzeScores(scores);
    }
    
    // 辅助方法
    private static void createNewFile() {
        System.out.println("创建新文件...");
    }
    
    private static void openExistingFile() {
        System.out.println("打开现有文件...");
    }
    
    private static void saveCurrentFile() {
        System.out.println("保存当前文件...");
    }
    
    private static boolean isValidEmail(String email) {
        return email.contains("@") && email.contains(".");
    }
    
    private static void analyzeScores(int[] scores) {
        int sum = 0;
        int max = scores[0];
        int min = scores[0];
        
        for (int score : scores) {
            sum += score;
            if (score > max) max = score;
            if (score < min) min = score;
        }
        
        double average = (double) sum / scores.length;
        System.out.println("平均分: " + String.format("%.2f", average));
        System.out.println("最高分: " + max);
        System.out.println("最低分: " + min);
    }
}