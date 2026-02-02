package com.opendemo.java.abstraction;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Java抽象概念演示程序
 * 展示抽象类、抽象方法、接口抽象、模板方法模式等核心概念
 */
public class AbstractionDemo {
    private static final Logger logger = LoggerFactory.getLogger(AbstractionDemo.class);
    
    public static void main(String[] args) {
        logger.info("=== Java抽象概念完整演示 ===");
        
        AbstractionDemo demo = new AbstractionDemo();
        
        demo.demonstrateAbstractClass();
        demo.demonstrateInterfaceAbstraction();
        demo.demonstrateTemplateMethodPattern();
        demo.demonstrateMultipleAbstraction();
        demo.demonstratePolymorphicAbstraction();
        
        logger.info("=== 演示完成 ===");
    }
    
    /**
     * 演示抽象类和抽象方法
     */
    public void demonstrateAbstractClass() {
        logger.info("--- 抽象类和抽象方法演示 ---");
        
        // 创建具体文档实例
        TextDocument textDoc = new TextDocument("Java学习笔记", "张三", 
            "Java是一门面向对象的编程语言。它具有封装、继承、多态等特性。");
        ImageDocument imageDoc = new ImageDocument("风景照片", "李四", 
            "/path/to/image.jpg", 1920, 1080, ImageDocument.ImageFormat.JPEG);
        
        // 调用具体方法
        logger.info("文档信息:");
        logger.info("  文本: {}", textDoc);
        logger.info("  图片: {}", imageDoc);
        
        // 调用抽象方法的具体实现
        logger.info("\n文档验证:");
        logger.info("  文本验证结果: {}", textDoc.validate() ? "✓ 通过" : "✗ 失败");
        logger.info("  图片验证结果: {}", imageDoc.validate() ? "✓ 通过" : "✗ 失败");
        
        // 文档特有方法
        logger.info("\n文档特有功能:");
        textDoc.normalizeWhitespace();
        textDoc.updateWordCount();
        logger.info("  文本字数: {}", textDoc.getWordCount());
        
        imageDoc.compress(80);
        logger.info("  图片压缩后大小: {} bytes", imageDoc.getFileSize());
        
        logger.info("");
    }
    
    /**
     * 演示接口抽象
     */
    public void demonstrateInterfaceAbstraction() {
        logger.info("--- 接口抽象演示 ---");
        
        // 创建可打印对象
        Report financialReport = new Report("季度财务报告", "财务部", 
            "第一季度收入增长15%，支出控制良好，净利润达到预期目标。", 
            Report.ReportType.FINANCIAL);
        
        Report technicalReport = new Report("系统架构设计", "技术部",
            "本系统采用微服务架构，包含用户服务、订单服务、支付服务等核心模块。", 
            Report.ReportType.TECHNICAL);
        
        // 调用接口方法
        logger.info("打印功能演示:");
        logger.info("  报告1页数: {}", financialReport.getPageCount());
        logger.info("  报告2页数: {}", technicalReport.getPageCount());
        
        // 使用默认方法
        logger.info("\n打印预览:");
        financialReport.printPreview();
        technicalReport.printPreview();
        
        // 使用带选项的打印
        logger.info("\n带选项打印:");
        Printable.PrintOptions options = new Printable.PrintOptions(true, true, 2, "HP_LaserJet");
        financialReport.printWithOptions(options);
        
        // 静态方法调用
        logger.info("\n批量打印:");
        Printable[] documents = {financialReport, technicalReport};
        Printable.printBatch(documents);
        
        logger.info("");
    }
    
    /**
     * 演示模板方法模式
     */
    public void demonstrateTemplateMethodPattern() {
        logger.info("--- 模板方法模式演示 ---");
        
        // 不同类型的文档使用相同的处理流程
        Document[] documents = {
            new TextDocument("模板测试1", "测试员", "这是测试内容"),
            new ImageDocument("模板测试2", "测试员", "/test/image.png", 800, 600, ImageDocument.ImageFormat.PNG),
            new Report("模板测试3", "测试员", "测试报告内容", Report.ReportType.TECHNICAL)
        };
        
        logger.info("统一文档处理流程:");
        for (Document doc : documents) {
            logger.info("\n处理文档: {}", doc.getClass().getSimpleName());
            logger.info("  处理前状态: {}", doc.getStatus());
            doc.processDocument();  // 调用模板方法
            logger.info("  处理后状态: {}", doc.getStatus());
        }
        
        logger.info("");
    }
    
    /**
     * 演示多重抽象（同时继承抽象类和实现接口）
     */
    public void demonstrateMultipleAbstraction() {
        logger.info("--- 多重抽象演示 ---");
        
        Report report = new Report("年度总结报告", "总经理办公室",
            "本年度公司在各个方面都取得了显著成绩。市场占有率提升20%，客户满意度达到95%。",
            Report.ReportType.MARKETING);
        
        // 通过不同引用类型访问
        logger.info("多重抽象特性演示:");
        
        // 1. 通过具体类引用
        logger.info("1. 通过Report引用:");
        report.generateSummary();
        report.addSection("未来规划", "明年计划拓展新市场，增加研发投入。");
        logger.info("  章节总数: {}", report.getSectionCount());
        
        // 2. 通过Document抽象类引用
        logger.info("\n2. 通过Document引用:");
        Document docRef = report;
        docRef.save();
        docRef.publish();
        logger.info("  文档状态: {}", docRef.getStatus());
        
        // 3. 通过Printable接口引用
        logger.info("\n3. 通过Printable引用:");
        Printable printRef = report;
        logger.info("  可打印性检查: {}", printRef.isPrintable() ? "✓ 可打印" : "✗ 不可打印");
        printRef.printPreview();
        
        logger.info("");
    }
    
    /**
     * 演示多态抽象
     */
    public void demonstratePolymorphicAbstraction() {
        logger.info("--- 多态抽象演示 ---");
        
        // 同一数组包含不同类型的抽象对象
        Document[] documents = {
            new TextDocument("文本文件", "作者A", "文本内容"),
            new ImageDocument("图片文件", "作者B", "/image/path.jpg", 1024, 768, ImageDocument.ImageFormat.JPEG),
            new Report("报告文件", "作者C", "报告内容", Report.ReportType.FINANCIAL)
        };
        
        logger.info("多态处理不同类型的文档:");
        for (Document doc : documents) {
            logger.info("\n处理 {}:", doc.getClass().getSimpleName());
            logger.info("  标题: {}", doc.getTitle());
            logger.info("  作者: {}", doc.getAuthor());
            logger.info("  验证结果: {}", doc.validate() ? "✓ 通过" : "✗ 失败");
            
            // 多态方法调用
            if (doc instanceof Printable) {
                Printable printable = (Printable) doc;
                logger.info("  页数: {}", printable.getPageCount());
                printable.printPreview();
            }
        }
        
        // 可打印对象的多态处理
        logger.info("\n可打印对象的多态处理:");
        Printable[] printables = {
            new Report("报告1", "作者1", "内容1", Report.ReportType.TECHNICAL),
            new Report("报告2", "作者2", "内容2", Report.ReportType.FINANCIAL)
        };
        
        for (Printable printable : printables) {
            logger.info("打印 {}: {} 页", 
                       printable.getClass().getSimpleName(), 
                       printable.getPageCount());
        }
        
        logger.info("");
    }
}