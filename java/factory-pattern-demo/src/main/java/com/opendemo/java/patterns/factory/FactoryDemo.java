package com.opendemo.java.patterns.factory;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class FactoryDemo {

    private static final Logger logger = LoggerFactory.getLogger(FactoryDemo.class);

    public static void main(String[] args) {
        logger.info("=== 工厂模式演示 ===");

        logger.info("--- 1. 简单工厂模式 ---");
        Document pdf = DocumentFactory.createDocument(DocumentType.PDF);
        pdf.open();
        pdf.save();
        pdf.close();

        Document word = DocumentFactory.createDocument(DocumentType.WORD);
        word.open();
        word.save();
        word.close();

        Document excel = DocumentFactory.createDocument(DocumentType.EXCEL);
        excel.open();
        excel.save();
        excel.close();

        logger.info("--- 2. 工厂方法模式 ---");
        AdvancedDocumentFactory pdfFactory = new PdfDocumentFactory();
        AdvancedDocumentFactory wordFactory = new WordDocumentFactory();
        AdvancedDocumentFactory excelFactory = new ExcelDocumentFactory();

        Document pdfDoc = pdfFactory.createDocument();
        Document wordDoc = wordFactory.createDocument();
        Document excelDoc = excelFactory.createDocument();

        logger.info("Created: {}", pdfDoc.getType());
        logger.info("Created: {}", wordDoc.getType());
        logger.info("Created: {}", excelDoc.getType());
    }

    public static class PdfDocumentFactory implements AdvancedDocumentFactory {
        @Override
        public Document createDocument() {
            return new PdfDocument();
        }
    }

    public static class WordDocumentFactory implements AdvancedDocumentFactory {
        @Override
        public Document createDocument() {
            return new WordDocument();
        }
    }

    public static class ExcelDocumentFactory implements AdvancedDocumentFactory {
        @Override
        public Document createDocument() {
            return new ExcelDocument();
        }
    }
}
