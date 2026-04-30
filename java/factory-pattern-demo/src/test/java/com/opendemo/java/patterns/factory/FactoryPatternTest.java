package com.opendemo.java.patterns.factory;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;

import static org.junit.jupiter.api.Assertions.*;

@DisplayName("工厂模式测试")
class FactoryPatternTest {

    @Test
    @DisplayName("简单工厂 - 创建PDF文档")
    void testCreatePdfDocument() {
        Document doc = DocumentFactory.createDocument(DocumentType.PDF);
        assertNotNull(doc);
        assertInstanceOf(PdfDocument.class, doc);
        assertEquals("PDF", doc.getType());
    }

    @Test
    @DisplayName("简单工厂 - 创建Word文档")
    void testCreateWordDocument() {
        Document doc = DocumentFactory.createDocument(DocumentType.WORD);
        assertNotNull(doc);
        assertInstanceOf(WordDocument.class, doc);
        assertEquals("WORD", doc.getType());
    }

    @Test
    @DisplayName("简单工厂 - 创建Excel文档")
    void testCreateExcelDocument() {
        Document doc = DocumentFactory.createDocument(DocumentType.EXCEL);
        assertNotNull(doc);
        assertInstanceOf(ExcelDocument.class, doc);
        assertEquals("EXCEL", doc.getType());
    }

    @Test
    @DisplayName("简单工厂 - 每次创建新实例")
    void testFactoryCreatesNewInstances() {
        Document doc1 = DocumentFactory.createDocument(DocumentType.PDF);
        Document doc2 = DocumentFactory.createDocument(DocumentType.PDF);
        assertNotSame(doc1, doc2);
    }

    @Test
    @DisplayName("工厂方法 - PDF工厂创建PDF文档")
    void testPdfDocumentFactory() {
        FactoryDemo.PdfDocumentFactory factory = new FactoryDemo.PdfDocumentFactory();
        Document doc = factory.createDocument();
        assertNotNull(doc);
        assertEquals("PDF", doc.getType());
    }

    @Test
    @DisplayName("工厂方法 - Word工厂创建Word文档")
    void testWordDocumentFactory() {
        FactoryDemo.WordDocumentFactory factory = new FactoryDemo.WordDocumentFactory();
        Document doc = factory.createDocument();
        assertNotNull(doc);
        assertEquals("WORD", doc.getType());
    }

    @Test
    @DisplayName("工厂方法 - Excel工厂创建Excel文档")
    void testExcelDocumentFactory() {
        FactoryDemo.ExcelDocumentFactory factory = new FactoryDemo.ExcelDocumentFactory();
        Document doc = factory.createDocument();
        assertNotNull(doc);
        assertEquals("EXCEL", doc.getType());
    }

    @Test
    @DisplayName("文档操作 - 完整生命周期")
    void testDocumentLifecycle() {
        Document doc = DocumentFactory.createDocument(DocumentType.PDF);
        assertDoesNotThrow(() -> {
            doc.open();
            doc.save();
            doc.close();
        });
    }

    @Test
    @DisplayName("文档类型枚举 - 所有类型")
    void testAllDocumentTypes() {
        DocumentType[] types = DocumentType.values();
        assertEquals(3, types.length);
        for (DocumentType type : types) {
            Document doc = DocumentFactory.createDocument(type);
            assertNotNull(doc);
        }
    }
}
