package com.opendemo.java.patterns.templatemethod;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class TemplateMethodDemo {

    private static final Logger logger = LoggerFactory.getLogger(TemplateMethodDemo.class);

    public static void main(String[] args) {
        logger.info("=== 模板方法模式演示 ===");

        logger.info("--- 1. 数据处理器 ---");
        DataProcessor csvProcessor = new CsvDataProcessor();
        csvProcessor.process("name,age,city");

        System.out.println();
        DataProcessor jsonProcessor = new JsonDataProcessor();
        jsonProcessor.process("{\"name\":\"Alice\",\"age\":30}");

        System.out.println();
        DataProcessor xmlProcessor = new XmlDataProcessor();
        xmlProcessor.process("<user><name>Bob</name></user>");

        logger.info("--- 2. 游戏模拟 ---");
        AbstractGame chess = new ChessGame();
        chess.play();

        System.out.println();
        AbstractGame football = new FootballGame();
        football.play();
    }
}
