package com.opendemo.java.abstraction;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Java抽象概念示例测试类
 * 测试抽象类、接口、模板方法等抽象概念的正确实现
 */
public class AbstractionDemoTest {
    private static final Logger logger = LoggerFactory.getLogger(AbstractionDemoTest.class);
    
    @BeforeEach
    void setUp() {
        logger.info("初始化抽象概念测试环境");
    }
    
    @Test
    void testAbstractClassImplementation() {
        logger.info("测试抽象类实现");
        
        // 测试TextDocument
        TextDocument textDoc = new TextDocument("测试文档", "测试作者", "测试内容文本");
        assertEquals("测试文档", textDoc.getTitle());
        assertEquals("测试作者", textDoc.getAuthor());
        assertEquals("测试内容文本", textDoc.getContent());
        assertEquals(2, textDoc.getWordCount());
        assertEquals("UTF-8", textDoc.getEncoding());
        
        // 测试ImageDocument
        ImageDocument imageDoc = new ImageDocument("测试图片", "图片作者", "/test/path.jpg", 
                                                  1920, 1080, ImageDocument.ImageFormat.PNG);
        assertEquals("测试图片", imageDoc.getTitle());
        assertEquals("图片作者", imageDoc.getAuthor());
        assertEquals("/test/path.jpg", imageDoc.getImagePath());
        assertEquals(1920, imageDoc.getWidth());
        assertEquals(1080, imageDoc.getHeight());
        assertEquals(ImageDocument.ImageFormat.PNG, imageDoc.getFormat());
        
        // 测试验证方法
        assertTrue(textDoc.validate());
        assertTrue(imageDoc.validate());
    }
    
    @Test
    void testAbstractMethodImplementation() {
        logger.info("测试抽象方法实现");
        
        TextDocument textDoc = new TextDocument("验证测试", "作者", "内容");
        ImageDocument imageDoc = new ImageDocument("验证测试", "作者", "/path", 800, 600, ImageDocument.ImageFormat.JPEG);
        
        // 验证抽象方法的具体实现
        assertDoesNotThrow(() -> textDoc.validate());
        assertDoesNotThrow(() -> imageDoc.validate());
        assertDoesNotThrow(() -> textDoc.execute());
        assertDoesNotThrow(() -> imageDoc.execute());
    }
    
    @Test
    void testInterfaceImplementation() {
        logger.info("测试接口实现");
        
        Report report = new Report("接口测试", "测试者", "测试内容", Report.ReportType.TECHNICAL);
        
        // 测试Printable接口方法
        assertNotNull(report.getPrintContent());
        assertTrue(report.getPrintContent().contains("接口测试"));
        assertTrue(report.getPageCount() > 0);
        assertTrue(report.isPrintable());
        
        // 测试默认方法
        assertDoesNotThrow(() -> report.printPreview());
        assertDoesNotThrow(() -> report.printWithOptions(null));
        
        Printable.PrintOptions options = new Printable.PrintOptions(true, true, 2, "测试打印机");
        assertDoesNotThrow(() -> report.printWithOptions(options));
    }
    
    @Test
    void testTemplateMethodPattern() {
        logger.info("测试模板方法模式");
        
        Document document = new TextDocument("模板测试", "作者", "内容");
        
        // 验证模板方法执行
        assertEquals(Document.DocumentStatus.DRAFT, document.getStatus());
        assertDoesNotThrow(() -> document.processDocument());
        assertEquals(Document.DocumentStatus.PROCESSED, document.getStatus());
        
        // 验证处理流程的各个步骤都被调用
        document.save();
        assertEquals(Document.DocumentStatus.SAVED, document.getStatus());
        
        document.publish();
        assertEquals(Document.DocumentStatus.PUBLISHED, document.getStatus());
    }
    
    @Test
    void testPolymorphicBehavior() {
        logger.info("测试多态行为");
        
        // 通过抽象类引用操作不同具体类型
        Document[] documents = {
            new TextDocument("文本", "作者1", "内容1"),
            new ImageDocument("图片", "作者2", "/path", 800, 600, ImageDocument.ImageFormat.JPEG),
            new Report("报告", "作者3", "内容3", Report.ReportType.FINANCIAL)
        };
        
        for (Document doc : documents) {
            // 验证多态方法调用
            assertTrue(doc.validate());
            assertDoesNotThrow(() -> doc.processDocument());
            
            // 验证类型特定的行为
            if (doc instanceof TextDocument) {
                TextDocument textDoc = (TextDocument) doc;
                textDoc.updateWordCount();
                assertTrue(textDoc.getWordCount() >= 0);
            }
            
            if (doc instanceof ImageDocument) {
                ImageDocument imageDoc = (ImageDocument) doc;
                assertTrue(imageDoc.isValidDimension());
            }
            
            if (doc instanceof Printable) {
                Printable printable = (Printable) doc;
                assertTrue(printable.isPrintable());
            }
        }
    }
    
    @Test
    void testMultipleInheritance() {
        logger.info("测试多重继承");
        
        Report report = new Report("多重继承测试", "作者", "内容", Report.ReportType.MARKETING);
        
        // 验证可以从不同引用类型访问
        Document docRef = report;
        Printable printRef = report;
        
        // Document方法
        assertEquals("多重继承测试", docRef.getTitle());
        assertEquals("作者", docRef.getAuthor());
        assertTrue(docRef.validate());
        
        // Printable方法
        assertTrue(printRef.isPrintable());
        assertTrue(printRef.getPageCount() > 0);
        assertNotNull(printRef.getPrintContent());
        
        // Report特有方法
        assertEquals(Report.ReportType.MARKETING, report.getReportType());
        assertTrue(report.getSectionCount() > 0);
    }
    
    @Test
    void testInterfaceStaticMethods() {
        logger.info("测试接口静态方法");
        
        Report report1 = new Report("报告1", "作者1", "内容1", Report.ReportType.TECHNICAL);
        Report report2 = new Report("报告2", "作者2", "内容2", Report.ReportType.FINANCIAL);
        
        Printable[] documents = {report1, report2};
        
        // 测试静态方法
        assertDoesNotThrow(() -> Printable.printBatch(documents));
        assertTrue(Printable.canPrint(report1));
        assertFalse(Printable.canPrint(null));
    }
    
    @Test
    void testDocumentStatusTransitions() {
        logger.info("测试文档状态转换");
        
        Document document = new TextDocument("状态测试", "作者", "内容");
        
        // 验证状态转换
        assertEquals(Document.DocumentStatus.DRAFT, document.getStatus());
        
        document.save();
        assertEquals(Document.DocumentStatus.SAVED, document.getStatus());
        
        document.processDocument();
        assertEquals(Document.DocumentStatus.PROCESSED, document.getStatus());
        
        document.publish();
        assertEquals(Document.DocumentStatus.PUBLISHED, document.getStatus());
        
        document.archive();
        assertEquals(Document.DocumentStatus.ARCHIVED, document.getStatus());
    }
    
    @Test
    void testTextDocumentSpecificFeatures() {
        logger.info("测试文本文档特有功能");
        
        TextDocument doc = new TextDocument("文本测试", "作者", "这是 测试  内容   ");
        
        // 测试文本处理功能
        doc.normalizeWhitespace();
        assertFalse(doc.getContent().contains("  "));
        
        doc.removeExtraSpaces();
        assertEquals(3, doc.getWordCount());
        
        assertTrue(doc.containsWord("测试"));
        assertEquals(1, doc.countOccurrences("测试"));
        
        doc.replaceText("测试", "检验");
        assertTrue(doc.containsWord("检验"));
        
        String summary = doc.getSummary(10);
        assertTrue(summary.length() <= 13); // 10 + "..."
    }
    
    @Test
    void testImageDocumentSpecificFeatures() {
        logger.info("测试图片文档特有功能");
        
        ImageDocument image = new ImageDocument("图片测试", "作者", "/path", 1920, 1080, ImageDocument.ImageFormat.JPEG);
        
        // 测试图片处理功能
        assertTrue(image.isLandscape());
        assertFalse(image.isPortrait());
        assertFalse(image.isSquare());
        
        assertEquals(1920.0/1080.0, image.getAspectRatio(), 0.01);
        assertEquals("1920×1080 pixels", image.getResolution());
        assertTrue(image.isValidDimension());
        
        image.resize(800, 600);
        assertEquals(800, image.getWidth());
        assertEquals(600, image.getHeight());
        
        image.compress(50);
        assertTrue(image.getFileSize() > 0);
    }
    
    @Test
    void testReportSpecificFeatures() {
        logger.info("测试报告特有功能");
        
        Report report = new Report("报告测试", "作者", "第一章内容\n\n第二章内容", Report.ReportType.TECHNICAL);
        
        // 测试报告功能
        assertEquals(2, report.getSectionCount());
        assertNotNull(report.getSection(0));
        assertNull(report.getSection(10)); // 越界访问
        
        assertTrue(report.containsSection("第一章"));
        assertFalse(report.containsSection("不存在的章节"));
        
        report.addSection("第三章", "新增章节内容");
        assertEquals(3, report.getSectionCount());
        
        Report copy = report.createCopy();
        assertEquals(report.getTitle(), copy.getTitle());
        assertEquals(report.getReportType(), copy.getReportType());
    }
    
    @Test
    void testValidationFailures() {
        logger.info("测试验证失败情况");
        
        // 测试无效的文档创建
        assertThrows(Exception.class, () -> {
            new TextDocument("", "作者", "内容");
        });
        
        assertThrows(Exception.class, () -> {
            new ImageDocument("标题", "作者", "", -1, -1, null);
        });
        
        // 测试验证失败的情况
        TextDocument invalidText = new TextDocument("测试", "作者", null);
        assertFalse(invalidText.validate());
        
        ImageDocument invalidImage = new ImageDocument("测试", "作者", "/path", 0, 0, ImageDocument.ImageFormat.JPEG);
        assertFalse(invalidImage.validate());
    }
}