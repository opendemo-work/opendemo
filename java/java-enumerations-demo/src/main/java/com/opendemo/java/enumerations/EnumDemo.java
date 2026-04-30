package com.opendemo.java.enumerations;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class EnumDemo {
    private static final Logger logger = LoggerFactory.getLogger(EnumDemo.class);

    public static void main(String[] args) {
        EnumDemo demo = new EnumDemo();
        demo.runAll();
    }

    public void runAll() {
        demonstrateColorEnum();
        demonstrateOperationEnum();
        demonstrateHttpStatusEnum();
        demonstrateSwitchStatement();
    }

    public void demonstrateColorEnum() {
        logger.info("=== 颜色枚举示例 ===");
        for (Color color : Color.values()) {
            logger.info("{}: {} - {} (主色: {})", color.name(), color.getName(), color.getHexCode(), color.isPrimary());
        }
        Color red = Color.RED;
        logger.info("通过名称查找: {}", Color.fromName("红色"));
        logger.info("通过代码查找: {}", Color.fromHexCode("#00FF00"));
    }

    public void demonstrateOperationEnum() {
        logger.info("=== 运算枚举示例 ===");
        double a = 10.0, b = 3.0;
        for (MathOperation op : MathOperation.values()) {
            logger.info("{} {} {} = {}", a, op.getSymbol(), b, op.apply(a, b));
        }
        MathOperation add = MathOperation.fromSymbol("+");
        logger.info("从符号查找: {} -> {}", "+", add.apply(5, 3));
    }

    public void demonstrateHttpStatusEnum() {
        logger.info("=== HTTP状态码枚举示例 ===");
        for (HttpStatus status : HttpStatus.values()) {
            logger.info("{} - 成功:{} 客户端错误:{} 服务端错误:{}",
                    status, status.isSuccess(), status.isClientError(), status.isServerError());
        }
        HttpStatus notFound = HttpStatus.fromCode(404);
        logger.info("404状态: {}", notFound);
    }

    public String demonstrateSwitchStatement() {
        logger.info("=== Switch语句示例 ===");
        Color color = Color.GREEN;
        String result;
        switch (color) {
            case RED:
                result = "选择了红色";
                break;
            case GREEN:
                result = "选择了绿色";
                break;
            case BLUE:
                result = "选择了蓝色";
                break;
            default:
                result = "选择了其他颜色";
                break;
        }
        logger.info(result);
        return result;
    }
}
