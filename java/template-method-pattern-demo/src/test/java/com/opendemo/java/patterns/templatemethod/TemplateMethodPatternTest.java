package com.opendemo.java.patterns.templatemethod;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;

import static org.junit.jupiter.api.Assertions.*;

@DisplayName("模板方法模式测试")
class TemplateMethodPatternTest {

    @Test
    @DisplayName("CSV处理器 - 正常处理")
    void testCsvProcessorNormal() {
        DataProcessor processor = new CsvDataProcessor();
        assertDoesNotThrow(() -> processor.process("name,age,city"));
    }

    @Test
    @DisplayName("CSV处理器 - 空数据抛出异常")
    void testCsvProcessorEmptyData() {
        DataProcessor processor = new CsvDataProcessor();
        assertThrows(IllegalArgumentException.class, () -> processor.process(""));
    }

    @Test
    @DisplayName("CSV处理器 - null数据抛出异常")
    void testCsvProcessorNullData() {
        DataProcessor processor = new CsvDataProcessor();
        assertThrows(IllegalArgumentException.class, () -> processor.process(null));
    }

    @Test
    @DisplayName("JSON处理器 - 正常处理")
    void testJsonProcessorNormal() {
        DataProcessor processor = new JsonDataProcessor();
        assertDoesNotThrow(() -> processor.process("{\"key\":\"value\"}"));
    }

    @Test
    @DisplayName("JSON处理器 - 无效数据抛出异常")
    void testJsonProcessorInvalidData() {
        DataProcessor processor = new JsonDataProcessor();
        assertThrows(IllegalArgumentException.class, () -> processor.process("not json"));
    }

    @Test
    @DisplayName("JSON处理器 - null数据抛出异常")
    void testJsonProcessorNullData() {
        DataProcessor processor = new JsonDataProcessor();
        assertThrows(IllegalArgumentException.class, () -> processor.process(null));
    }

    @Test
    @DisplayName("XML处理器 - 正常处理")
    void testXmlProcessorNormal() {
        DataProcessor processor = new XmlDataProcessor();
        assertDoesNotThrow(() -> processor.process("<root><item>test</item></root>"));
    }

    @Test
    @DisplayName("XML处理器 - 无效数据抛出异常")
    void testXmlProcessorInvalidData() {
        DataProcessor processor = new XmlDataProcessor();
        assertThrows(IllegalArgumentException.class, () -> processor.process("not xml"));
    }

    @Test
    @DisplayName("国际象棋 - 正常游戏流程")
    void testChessGamePlay() {
        AbstractGame chess = new ChessGame();
        assertDoesNotThrow(chess::play);
    }

    @Test
    @DisplayName("足球 - 正常游戏流程")
    void testFootballGamePlay() {
        AbstractGame football = new FootballGame();
        assertDoesNotThrow(football::play);
    }

    @Test
    @DisplayName("所有处理器继承自DataProcessor")
    void testProcessorInheritance() {
        assertTrue(new CsvDataProcessor() instanceof DataProcessor);
        assertTrue(new JsonDataProcessor() instanceof DataProcessor);
        assertTrue(new XmlDataProcessor() instanceof DataProcessor);
    }

    @Test
    @DisplayName("所有游戏继承自AbstractGame")
    void testGameInheritance() {
        assertTrue(new ChessGame() instanceof AbstractGame);
        assertTrue(new FootballGame() instanceof AbstractGame);
    }
}
