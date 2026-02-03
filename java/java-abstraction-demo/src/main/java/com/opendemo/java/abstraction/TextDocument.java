package com.opendemo.java.abstraction;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * TextDocument文本文档类 - 演示具体实现抽象类
 * 实现文本文档特有的处理逻辑
 */
public class TextDocument extends Document {
    private static final Logger logger = LoggerFactory.getLogger(TextDocument.class);
    
    private String content;
    private String encoding;
    private int wordCount;
    
    // 构造方法
    public TextDocument(String title, String author, String content) {
        super(title, author);
        this.content = content != null ? content : "";
        this.encoding = "UTF-8";
        this.wordCount = calculateWordCount();
        logger.info("创建文本文档: {}, 字数: {}", title, wordCount);
    }
    
    public TextDocument(String title, String author, String content, String encoding) {
        this(title, author, content);
        this.encoding = encoding;
        logger.info("创建{}编码的文本文档: {}", encoding, title);
    }
    
    // Getter和Setter方法
    public String getContent() {
        return content;
    }
    
    public void setContent(String content) {
        this.content = content != null ? content : "";
        this.wordCount = calculateWordCount();
        logger.info("更新文本内容，新字数: {}", wordCount);
    }
    
    public String getEncoding() {
        return encoding;
    }
    
    public void setEncoding(String encoding) {
        this.encoding = encoding;
        logger.info("文档编码更新为: {}", encoding);
    }
    
    public int getWordCount() {
        return wordCount;
    }
    
    // 实现抽象方法
    @Override
    public boolean validate() {
        logger.info("验证文本文档: {}", title);
        
        // 验证标题
        if (title == null || title.trim().isEmpty()) {
            logger.error("文档标题不能为空");
            return false;
        }
        
        // 验证作者
        if (author == null || author.trim().isEmpty()) {
            logger.error("文档作者不能为空");
            return false;
        }
        
        // 验证内容
        if (content == null) {
            logger.error("文档内容不能为空");
            return false;
        }
        
        // 验证编码
        if (encoding == null || encoding.trim().isEmpty()) {
            logger.error("文档编码不能为空");
            return false;
        }
        
        logger.info("文本文档验证通过");
        return true;
    }
    
    @Override
    protected void execute() {
        logger.info("执行文本文档处理: {}", title);
        
        // 文本处理的具体实现
        normalizeWhitespace();
        removeExtraSpaces();
        updateWordCount();
        
        logger.info("文本处理完成，最终字数: {}", wordCount);
    }
    
    // 重写钩子方法
    @Override
    protected void prepare() {
        logger.info("准备文本处理环境");
        logger.info("原文档字数: {}", wordCount);
    }
    
    @Override
    protected void cleanup() {
        logger.info("清理文本处理资源");
        logger.info("处理后文档字数: {}", wordCount);
    }
    
    // 文本特有方法
    public void normalizeWhitespace() {
        if (content != null) {
            content = content.replaceAll("\\s+", " ").trim();
            logger.info("规范化空白字符");
        }
    }
    
    public void removeExtraSpaces() {
        if (content != null) {
            content = content.replaceAll(" +", " ");
            logger.info("移除多余空格");
        }
    }
    
    public void updateWordCount() {
        wordCount = calculateWordCount();
        logger.info("更新字数统计: {}", wordCount);
    }
    
    public boolean containsWord(String word) {
        if (content == null || word == null) return false;
        return content.toLowerCase().contains(word.toLowerCase());
    }
    
    public int countOccurrences(String word) {
        if (content == null || word == null || word.isEmpty()) return 0;
        
        String lowerContent = content.toLowerCase();
        String lowerWord = word.toLowerCase();
        int count = 0;
        int index = 0;
        
        while ((index = lowerContent.indexOf(lowerWord, index)) != -1) {
            count++;
            index += lowerWord.length();
        }
        
        return count;
    }
    
    public String getSummary(int maxLength) {
        if (content == null || content.isEmpty()) {
            return "";
        }
        
        if (content.length() <= maxLength) {
            return content;
        }
        
        String summary = content.substring(0, maxLength);
        int lastSpace = summary.lastIndexOf(' ');
        if (lastSpace > 0) {
            summary = summary.substring(0, lastSpace);
        }
        
        return summary + "...";
    }
    
    public void appendContent(String additionalContent) {
        if (additionalContent != null) {
            content += additionalContent;
            wordCount = calculateWordCount();
            logger.info("追加内容，新字数: {}", wordCount);
        }
    }
    
    public void replaceText(String target, String replacement) {
        if (content != null && target != null && replacement != null) {
            int occurrences = countOccurrences(target);
            content = content.replace(target, replacement);
            wordCount = calculateWordCount();
            logger.info("替换了 {} 处 '{}' 为 '{}'", occurrences, target, replacement);
        }
    }
    
    // 私有辅助方法
    private int calculateWordCount() {
        if (content == null || content.trim().isEmpty()) {
            return 0;
        }
        String[] words = content.trim().split("\\s+");
        return words.length;
    }
    
    // 重写toString方法
    @Override
    public String toString() {
        return String.format("TextDocument{title='%s', author='%s', words=%d, encoding='%s', status=%s}", 
                           title, author, wordCount, encoding, status);
    }
    
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        if (!super.equals(obj)) return false;
        
        TextDocument that = (TextDocument) obj;
        return wordCount == that.wordCount &&
               content.equals(that.content) &&
               encoding.equals(that.encoding);
    }
    
    @Override
    public int hashCode() {
        int result = super.hashCode();
        result = 31 * result + content.hashCode();
        result = 31 * result + encoding.hashCode();
        result = 31 * result + wordCount;
        return result;
    }
}