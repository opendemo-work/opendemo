package com.opendemo.java.innerclasses;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class OuterClass {
    private static final Logger logger = LoggerFactory.getLogger(OuterClass.class);

    private String outerField = "外部类字段";
    private static String staticOuterField = "静态外部类字段";

    public class InnerClass {
        private String innerField = "成员内部类字段";

        public String getOuterField() {
            return outerField;
        }

        public String getInnerField() {
            return innerField;
        }

        public void accessOuter() {
            logger.info("成员内部类访问外部类字段: {}", outerField);
            logger.info("成员内部类访问外部类静态字段: {}", staticOuterField);
        }
    }

    public static class StaticNestedClass {
        private String nestedField = "静态嵌套类字段";

        public String getNestedField() {
            return nestedField;
        }

        public void display() {
            logger.info("静态嵌套类 - 只能访问静态外部类字段: {}", staticOuterField);
        }

        public static void staticMethod() {
            logger.info("静态嵌套类的静态方法");
        }
    }

    public String getOuterField() {
        return outerField;
    }

    public InnerClass createInner() {
        return new InnerClass();
    }

    public String demonstrateLocalClass(String prefix) {
        class LocalClass {
            private String localField = "局部内部类字段";

            String process(String input) {
                return prefix + " - " + input + " - " + localField;
            }
        }
        LocalClass local = new LocalClass();
        return local.process("局部内部类处理结果");
    }

    public Runnable createAnonymousRunnable(String message) {
        return new Runnable() {
            private String anonymousField = "匿名内部类字段";

            @Override
            public void run() {
                logger.info("匿名内部类执行: {} - {}", message, anonymousField);
            }
        };
    }
}
