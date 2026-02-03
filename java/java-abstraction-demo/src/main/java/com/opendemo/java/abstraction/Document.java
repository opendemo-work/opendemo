package com.opendemo.java.abstraction;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.time.LocalDateTime;

/**
 * Document抽象类 - 演示抽象类和抽象方法
 * 定义文档处理的通用框架和抽象行为
 */
public abstract class Document {
    protected static final Logger logger = LoggerFactory.getLogger(Document.class);
    
    // 受保护的成员变量
    protected String title;
    protected String author;
    protected LocalDateTime createdAt;
    protected DocumentStatus status;
    
    // 构造方法
    public Document(String title, String author) {
        this.title = title;
        this.author = author;
        this.createdAt = LocalDateTime.now();
        this.status = DocumentStatus.DRAFT;
        logger.info("创建文档: {}, 作者: {}", title, author);
    }
    
    // 具体方法 - 提供通用实现
    public void setTitle(String title) {
        if (title != null && !title.trim().isEmpty()) {
            String oldTitle = this.title;
            this.title = title.trim();
            logger.info("文档标题从 '{}' 更新为 '{}'", oldTitle, this.title);
        } else {
            logger.warn("文档标题不能为空");
        }
    }
    
    public void setAuthor(String author) {
        if (author != null && !author.trim().isEmpty()) {
            String oldAuthor = this.author;
            this.author = author.trim();
            logger.info("文档作者从 '{}' 更新为 '{}'", oldAuthor, this.author);
        } else {
            logger.warn("文档作者不能为空");
        }
    }
    
    public String getTitle() {
        return title;
    }
    
    public String getAuthor() {
        return author;
    }
    
    public LocalDateTime getCreatedAt() {
        return createdAt;
    }
    
    public DocumentStatus getStatus() {
        return status;
    }
    
    // 模板方法 - 定义文档处理的标准流程
    public final void processDocument() {
        logger.info("开始处理文档: {}", title);
        
        if (validate()) {
            prepare();
            execute();
            cleanup();
            status = DocumentStatus.PROCESSED;
            logger.info("文档处理完成: {}", title);
        } else {
            status = DocumentStatus.ERROR;
            logger.error("文档验证失败，处理终止: {}", title);
        }
    }
    
    // 钩子方法 - 子类可以选择性重写
    protected void prepare() {
        logger.info("准备文档处理环境");
    }
    
    protected void cleanup() {
        logger.info("清理文档处理资源");
    }
    
    // 抽象方法 - 子类必须实现的具体行为
    public abstract boolean validate();
    protected abstract void execute();
    
    // 具体的通用方法
    public void save() {
        logger.info("保存文档: {}", title);
        status = DocumentStatus.SAVED;
    }
    
    public void publish() {
        if (status == DocumentStatus.SAVED || status == DocumentStatus.DRAFT) {
            logger.info("发布文档: {}", title);
            status = DocumentStatus.PUBLISHED;
        } else {
            logger.warn("文档状态不允许发布: {}", status);
        }
    }
    
    public void archive() {
        logger.info("归档文档: {}", title);
        status = DocumentStatus.ARCHIVED;
    }
    
    // 重写Object方法
    @Override
    public String toString() {
        return String.format("%s{title='%s', author='%s', status=%s, created=%s}", 
                           getClass().getSimpleName(), title, author, status, createdAt.toLocalDate());
    }
    
    // 文档状态枚举
    public enum DocumentStatus {
        DRAFT("草稿"),
        SAVED("已保存"),
        PROCESSING("处理中"),
        PROCESSED("已处理"),
        PUBLISHED("已发布"),
        ARCHIVED("已归档"),
        ERROR("错误");
        
        private final String description;
        
        DocumentStatus(String description) {
            this.description = description;
        }
        
        public String getDescription() {
            return description;
        }
    }
}