package com.opendemo.java.patterns.singleton;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class SingletonDemo {

    private static final Logger logger = LoggerFactory.getLogger(SingletonDemo.class);

    public static void main(String[] args) {
        logger.info("=== 单例模式演示 ===");

        logger.info("--- 1. 饿汉式单例 ---");
        EagerSingleton eager1 = EagerSingleton.getInstance();
        EagerSingleton eager2 = EagerSingleton.getInstance();
        logger.info(eager1.getInfo());
        logger.info("是否同一实例: {}", eager1 == eager2);

        logger.info("--- 2. 懒汉式单例 ---");
        LazySingleton lazy1 = LazySingleton.getInstance();
        LazySingleton lazy2 = LazySingleton.getInstance();
        logger.info(lazy1.getInfo());
        logger.info("是否同一实例: {}", lazy1 == lazy2);

        logger.info("--- 3. 双重检查锁定单例 ---");
        ThreadSafeSingleton threadSafe1 = ThreadSafeSingleton.getInstance();
        ThreadSafeSingleton threadSafe2 = ThreadSafeSingleton.getInstance();
        logger.info(threadSafe1.getInfo());
        logger.info("是否同一实例: {}", threadSafe1 == threadSafe2);

        logger.info("--- 4. 枚举式单例 ---");
        EnumSingleton enum1 = EnumSingleton.INSTANCE;
        EnumSingleton enum2 = EnumSingleton.INSTANCE;
        logger.info(enum1.getInfo());
        logger.info("是否同一实例: {}", enum1 == enum2);
        logger.info("计数器: {}", enum1.increment());
        logger.info("计数器: {}", enum2.increment());

        logger.info("--- 5. 静态内部类单例 ---");
        InnerClassSingleton inner1 = InnerClassSingleton.getInstance();
        InnerClassSingleton inner2 = InnerClassSingleton.getInstance();
        logger.info(inner1.getInfo());
        logger.info("是否同一实例: {}", inner1 == inner2);
    }
}
