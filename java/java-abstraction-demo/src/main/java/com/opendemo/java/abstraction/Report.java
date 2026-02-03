package com.opendemo.java.abstraction;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * Report报告类 - 演示同时继承抽象类和实现接口
 * 结合文档抽象和打印接口的功能
 */
public class Report extends Document implements Printable {
    private static final Logger logger = LoggerFactory.getLogger(Report.class);
    
    private String content;
    private ReportType reportType;
    private LocalDateTime generatedAt;
    private String[] sections;
    
    // 构造方法
    public Report(String title, String author, String content, ReportType reportType) {
        super(title, author);
        this.content = content != null ? content : "";
        this.reportType = reportType;
        this.generatedAt = LocalDateTime.now();
        this.sections = parseSections(content);
        logger.info("创建{}报告: {}, 包含 {} 个章节", reportType.getDescription(), title, sections.length);
    }
    
    // Getter和Setter方法
    public String getContent() {
        return content;
    }
    
    public void setContent(String content) {
        this.content = content != null ? content : "";
        this.sections = parseSections(this.content);
        logger.info("更新报告内容，新章节数: {}", sections.length);
    }
    
    public ReportType getReportType() {
        return reportType;
    }
    
    public void setReportType(ReportType reportType) {
        this.reportType = reportType;
        logger.info("报告类型更新为: {}", reportType.getDescription());
    }
    
    public LocalDateTime getGeneratedAt() {
        return generatedAt;
    }
    
    public String[] getSections() {
        return sections.clone(); // 返回拷贝防止外部修改
    }
    
    // 实现Document抽象方法
    @Override
    public boolean validate() {
        logger.info("验证报告: {}", title);
        
        // 验证基本文档属性
        if (!super.validate()) {
            return false;
        }
        
        // 验证报告特定属性
        if (reportType == null) {
            logger.error("报告类型不能为空");
            return false;
        }
        
        if (content == null || content.trim().isEmpty()) {
            logger.error("报告内容不能为空");
            return false;
        }
        
        logger.info("报告验证通过");
        return true;
    }
    
    @Override
    protected void execute() {
        logger.info("执行报告生成: {}", title);
        
        // 报告生成的具体实现
        formatContent();
        addPageNumbers();
        generateTableOfContents();
        
        logger.info("报告生成完成，共 {} 页", getPageCount());
    }
    
    // 重写钩子方法
    @Override
    protected void prepare() {
        logger.info("准备报告生成环境");
        logger.info("报告类型: {}, 原始章节数: {}", reportType.getDescription(), sections.length);
    }
    
    @Override
    protected void cleanup() {
        logger.info("清理报告生成资源");
        logger.info("最终页数: {}", getPageCount());
    }
    
    // 实现Printable接口方法
    @Override
    public void print() {
        logger.info("打印报告: {}", title);
        logger.info("报告类型: {}", reportType.getDescription());
        logger.info("生成时间: {}", generatedAt.format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")));
        logger.info("内容预览: {}", getPrintContent().substring(0, Math.min(100, getPrintContent().length())));
        status = DocumentStatus.PROCESSED;
    }
    
    @Override
    public String getPrintContent() {
        StringBuilder printContent = new StringBuilder();
        printContent.append("报告标题: ").append(title).append("\n");
        printContent.append("作者: ").append(author).append("\n");
        printContent.append("类型: ").append(reportType.getDescription()).append("\n");
        printContent.append("生成时间: ").append(generatedAt.format(DateTimeFormatter.ISO_LOCAL_DATE)).append("\n");
        printContent.append("--- 报告内容 ---\n");
        printContent.append(content);
        return printContent.toString();
    }
    
    @Override
    public int getPageCount() {
        // 简单的页数计算：每页约500字
        if (content == null || content.isEmpty()) {
            return 1; // 至少一页封面
        }
        return Math.max(1, (int) Math.ceil(content.length() / 500.0));
    }
    
    // 报告特有方法
    public void addSection(String sectionTitle, String sectionContent) {
        if (sectionTitle != null && sectionContent != null) {
            content += "\n\n" + sectionTitle + "\n" + "=".repeat(sectionTitle.length()) + "\n" + sectionContent;
            sections = parseSections(content);
            logger.info("添加章节: {}, 当前总章节数: {}", sectionTitle, sections.length);
        }
    }
    
    public String getSection(int index) {
        if (index >= 0 && index < sections.length) {
            return sections[index];
        }
        return null;
    }
    
    public int getSectionCount() {
        return sections.length;
    }
    
    public boolean containsSection(String sectionTitle) {
        if (sectionTitle == null || content == null) return false;
        return content.toLowerCase().contains(sectionTitle.toLowerCase());
    }
    
    public void generateSummary() {
        logger.info("生成报告摘要");
        String summary = content.length() > 200 ? content.substring(0, 200) + "..." : content;
        logger.info("报告摘要: {}", summary);
    }
    
    public Report createCopy() {
        Report copy = new Report(title, author, content, reportType);
        copy.status = this.status;
        return copy;
    }
    
    public void mergeWith(Report other) {
        if (other != null && other.reportType == this.reportType) {
            this.content += "\n\n" + other.content;
            this.sections = parseSections(this.content);
            logger.info("合并报告，新章节总数: {}", sections.length);
        } else {
            logger.warn("只能合并相同类型的报告");
        }
    }
    
    // 私有辅助方法
    private void formatContent() {
        logger.info("格式化报告内容");
        // 模拟内容格式化
        content = content.replaceAll("\n{3,}", "\n\n"); // 规范换行
    }
    
    private void addPageNumbers() {
        logger.info("添加页码");
        // 模拟页码添加
    }
    
    private void generateTableOfContents() {
        logger.info("生成目录");
        // 模拟目录生成
    }
    
    private String[] parseSections(String content) {
        if (content == null || content.isEmpty()) {
            return new String[0];
        }
        
        // 简单的章节解析：以两个换行符分割
        return content.split("\n{2,}");
    }
    
    // 重写toString方法
    @Override
    public String toString() {
        return String.format("Report{title='%s', author='%s', type=%s, sections=%d, pages=%d, status=%s}", 
                           title, author, reportType, sections.length, getPageCount(), status);
    }
    
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        if (!super.equals(obj)) return false;
        
        Report report = (Report) obj;
        return reportType == report.reportType &&
               content.equals(report.content) &&
               generatedAt.equals(report.generatedAt);
    }
    
    @Override
    public int hashCode() {
        int result = super.hashCode();
        result = 31 * result + content.hashCode();
        result = 31 * result + reportType.hashCode();
        result = 31 * result + generatedAt.hashCode();
        return result;
    }
    
    // 报告类型枚举
    public enum ReportType {
        FINANCIAL("财务报告"),
        TECHNICAL("技术报告"),
        MARKETING("市场报告"),
        HR("人力资源报告"),
        PROJECT("项目报告");
        
        private final String description;
        
        ReportType(String description) {
            this.description = description;
        }
        
        public String getDescription() {
            return description;
        }
    }
}