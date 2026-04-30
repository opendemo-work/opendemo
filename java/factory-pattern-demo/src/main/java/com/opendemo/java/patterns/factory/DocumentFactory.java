package com.opendemo.java.patterns.factory;

public class DocumentFactory {

    public static Document createDocument(DocumentType type) {
        switch (type) {
            case PDF:
                return new PdfDocument();
            case WORD:
                return new WordDocument();
            case EXCEL:
                return new ExcelDocument();
            default:
                throw new IllegalArgumentException("Unknown document type: " + type);
        }
    }
}
