package com.opendemo.java.abstraction;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Printable接口 - 演示接口抽象
 * 定义可打印对象的标准行为
 */
public interface Printable {
    Logger logger = LoggerFactory.getLogger(Printable.class);
    
    // 抽象方法
    void print();
    String getPrintContent();
    int getPageCount();
    
    // 默认方法 - Java 8+特性
    default void printPreview() {
        logger.info("打印预览:");
        logger.info("内容: {}", getPrintContent());
        logger.info("页数: {}", getPageCount());
    }
    
    default boolean isPrintable() {
        return getPrintContent() != null && !getPrintContent().isEmpty() && getPageCount() > 0;
    }
    
    default void printWithOptions(PrintOptions options) {
        if (options == null) {
            print();
            return;
        }
        
        logger.info("使用选项打印: {}", options);
        if (options.isPreview()) {
            printPreview();
        }
        if (options.isDoubleSided()) {
            logger.info("启用双面打印");
        }
        if (options.getCopies() > 1) {
            logger.info("打印 {} 份", options.getCopies());
        }
        print();
    }
    
    // 静态方法 - Java 8+特性
    static void printBatch(Printable[] documents) {
        if (documents == null || documents.length == 0) {
            logger.warn("没有文档需要打印");
            return;
        }
        
        logger.info("开始批量打印 {} 个文档", documents.length);
        int totalPages = 0;
        
        for (int i = 0; i < documents.length; i++) {
            Printable doc = documents[i];
            logger.info("打印第 {} 个文档: {}", i + 1, doc.getClass().getSimpleName());
            doc.print();
            totalPages += doc.getPageCount();
        }
        
        logger.info("批量打印完成，总共 {} 页", totalPages);
    }
    
    static boolean canPrint(Printable document) {
        return document != null && document.isPrintable();
    }
    
    // 私有方法 - Java 9+特性
    private void logPrintOperation(String operation) {
        logger.info("执行打印操作: {}", operation);
    }
    
    // 私有静态方法 - Java 9+特性
    private static void validatePrintRequest(Printable document) {
        if (document == null) {
            throw new IllegalArgumentException("文档不能为空");
        }
        if (!document.isPrintable()) {
            throw new IllegalStateException("文档不可打印");
        }
    }
    
    // 打印选项类
    class PrintOptions {
        private boolean preview = false;
        private boolean doubleSided = false;
        private int copies = 1;
        private String printerName;
        
        public PrintOptions() {}
        
        public PrintOptions(boolean preview, boolean doubleSided, int copies, String printerName) {
            this.preview = preview;
            this.doubleSided = doubleSided;
            this.copies = copies;
            this.printerName = printerName;
        }
        
        // Getter和Setter方法
        public boolean isPreview() { return preview; }
        public void setPreview(boolean preview) { this.preview = preview; }
        
        public boolean isDoubleSided() { return doubleSided; }
        public void setDoubleSided(boolean doubleSided) { this.doubleSided = doubleSided; }
        
        public int getCopies() { return copies; }
        public void setCopies(int copies) { 
            if (copies > 0) this.copies = copies; 
        }
        
        public String getPrinterName() { return printerName; }
        public void setPrinterName(String printerName) { this.printerName = printerName; }
        
        @Override
        public String toString() {
            return String.format("PrintOptions{preview=%s, doubleSided=%s, copies=%d, printer='%s'}", 
                               preview, doubleSided, copies, printerName);
        }
    }
}