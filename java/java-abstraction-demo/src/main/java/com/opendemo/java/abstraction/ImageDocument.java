package com.opendemo.java.abstraction;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * ImageDocument图片文档类 - 演示另一种具体实现
 * 实现图片文档特有的处理逻辑
 */
public class ImageDocument extends Document {
    private static final Logger logger = LoggerFactory.getLogger(ImageDocument.class);
    
    private String imagePath;
    private int width;
    private int height;
    private ImageFormat format;
    private long fileSize; // bytes
    
    // 构造方法
    public ImageDocument(String title, String author, String imagePath, int width, int height, ImageFormat format) {
        super(title, author);
        this.imagePath = imagePath;
        this.width = width;
        this.height = height;
        this.format = format;
        this.fileSize = 0;
        logger.info("创建图片文档: {}, 尺寸: {}×{}, 格式: {}", title, width, height, format);
    }
    
    // Getter和Setter方法
    public String getImagePath() {
        return imagePath;
    }
    
    public void setImagePath(String imagePath) {
        this.imagePath = imagePath;
        logger.info("更新图片路径: {}", imagePath);
    }
    
    public int getWidth() {
        return width;
    }
    
    public void setWidth(int width) {
        if (width > 0) {
            this.width = width;
            logger.info("更新图片宽度: {}", width);
        } else {
            logger.warn("图片宽度必须大于0: {}", width);
        }
    }
    
    public int getHeight() {
        return height;
    }
    
    public void setHeight(int height) {
        if (height > 0) {
            this.height = height;
            logger.info("更新图片高度: {}", height);
        } else {
            logger.warn("图片高度必须大于0: {}", height);
        }
    }
    
    public ImageFormat getFormat() {
        return format;
    }
    
    public void setFormat(ImageFormat format) {
        this.format = format;
        logger.info("更新图片格式: {}", format);
    }
    
    public long getFileSize() {
        return fileSize;
    }
    
    public void setFileSize(long fileSize) {
        if (fileSize >= 0) {
            this.fileSize = fileSize;
            logger.info("更新文件大小: {} bytes ({})", fileSize, formatFileSize(fileSize));
        } else {
            logger.warn("文件大小不能为负数: {}", fileSize);
        }
    }
    
    // 实现抽象方法
    @Override
    public boolean validate() {
        logger.info("验证图片文档: {}", title);
        
        // 验证基本属性
        if (title == null || title.trim().isEmpty()) {
            logger.error("文档标题不能为空");
            return false;
        }
        
        if (author == null || author.trim().isEmpty()) {
            logger.error("文档作者不能为空");
            return false;
        }
        
        // 验证图片路径
        if (imagePath == null || imagePath.trim().isEmpty()) {
            logger.error("图片路径不能为空");
            return false;
        }
        
        // 验证尺寸
        if (width <= 0 || height <= 0) {
            logger.error("图片尺寸必须大于0: {}×{}", width, height);
            return false;
        }
        
        // 验证格式
        if (format == null) {
            logger.error("图片格式不能为空");
            return false;
        }
        
        logger.info("图片文档验证通过");
        return true;
    }
    
    @Override
    protected void execute() {
        logger.info("执行图片文档处理: {}", title);
        
        // 图片处理的具体实现
        optimizeImage();
        updateFileSize();
        generateThumbnail();
        
        logger.info("图片处理完成，文件大小: {}", formatFileSize(fileSize));
    }
    
    // 重写钩子方法
    @Override
    protected void prepare() {
        logger.info("准备图片处理环境");
        logger.info("原始尺寸: {}×{}, 格式: {}", width, height, format);
    }
    
    @Override
    protected void cleanup() {
        logger.info("清理图片处理资源");
        logger.info("最终文件大小: {}", formatFileSize(fileSize));
    }
    
    // 图片特有方法
    public void resize(int newWidth, int newHeight) {
        if (newWidth > 0 && newHeight > 0) {
            logger.info("调整图片尺寸从 {}×{} 到 {}×{}", width, height, newWidth, newHeight);
            this.width = newWidth;
            this.height = newHeight;
        } else {
            logger.warn("新尺寸必须大于0: {}×{}", newWidth, newHeight);
        }
    }
    
    public void rotate(double degrees) {
        logger.info("旋转图片 {} 度", degrees);
        // 实际的旋转逻辑会涉及像素重新排列
        // 这里只是演示日志记录
    }
    
    public void crop(int x, int y, int cropWidth, int cropHeight) {
        if (x >= 0 && y >= 0 && cropWidth > 0 && cropHeight > 0) {
            logger.info("裁剪图片: 从({}, {})裁剪 {}×{}", x, y, cropWidth, cropHeight);
            // 更新尺寸信息
            this.width = cropWidth;
            this.height = cropHeight;
        } else {
            logger.warn("裁剪参数无效: ({}, {}) {}×{}", x, y, cropWidth, cropHeight);
        }
    }
    
    public void compress(int quality) {
        if (quality >= 0 && quality <= 100) {
            logger.info("压缩图片，质量: {}%", quality);
            long originalSize = fileSize;
            // 模拟压缩效果
            fileSize = (long) (fileSize * (quality / 100.0) * 0.8);
            logger.info("压缩后文件大小: {} (减少 {})", 
                       formatFileSize(fileSize), 
                       formatFileSize(originalSize - fileSize));
        } else {
            logger.warn("压缩质量必须在0-100之间: {}", quality);
        }
    }
    
    public boolean isPortrait() {
        return height > width;
    }
    
    public boolean isLandscape() {
        return width > height;
    }
    
    public boolean isSquare() {
        return width == height;
    }
    
    public double getAspectRatio() {
        return (double) width / height;
    }
    
    public String getResolution() {
        return width + "×" + height + " pixels";
    }
    
    public boolean isValidDimension() {
        return width > 0 && height > 0 && width <= 10000 && height <= 10000;
    }
    
    // 私有辅助方法
    private void optimizeImage() {
        logger.info("优化图片质量");
        // 模拟优化过程
    }
    
    private void updateFileSize() {
        // 模拟基于尺寸和格式计算文件大小
        long baseSize = (long) (width * height * format.getBitsPerPixel() / 8);
        fileSize = baseSize;
        logger.info("计算文件大小: {}", formatFileSize(fileSize));
    }
    
    private void generateThumbnail() {
        int thumbWidth = Math.min(150, width / 4);
        int thumbHeight = Math.min(150, height / 4);
        logger.info("生成缩略图: {}×{}", thumbWidth, thumbHeight);
    }
    
    private String formatFileSize(long bytes) {
        if (bytes < 1024) return bytes + " B";
        if (bytes < 1024 * 1024) return String.format("%.1f KB", bytes / 1024.0);
        return String.format("%.1f MB", bytes / (1024.0 * 1024));
    }
    
    // 重写toString方法
    @Override
    public String toString() {
        return String.format("ImageDocument{title='%s', author='%s', size=%s, format=%s, status=%s}", 
                           title, author, getResolution(), format, status);
    }
    
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        if (!super.equals(obj)) return false;
        
        ImageDocument that = (ImageDocument) obj;
        return width == that.width &&
               height == that.height &&
               fileSize == that.fileSize &&
               imagePath.equals(that.imagePath) &&
               format == that.format;
    }
    
    @Override
    public int hashCode() {
        int result = super.hashCode();
        result = 31 * result + imagePath.hashCode();
        result = 31 * result + width;
        result = 31 * result + height;
        result = 31 * result + format.hashCode();
        result = 31 * result + (int) (fileSize ^ (fileSize >>> 32));
        return result;
    }
    
    // 图片格式枚举
    public enum ImageFormat {
        JPEG("JPEG", 24),
        PNG("PNG", 32),
        GIF("GIF", 8),
        BMP("BMP", 24),
        TIFF("TIFF", 32);
        
        private final String name;
        private final int bitsPerPixel;
        
        ImageFormat(String name, int bitsPerPixel) {
            this.name = name;
            this.bitsPerPixel = bitsPerPixel;
        }
        
        public String getName() {
            return name;
        }
        
        public int getBitsPerPixel() {
            return bitsPerPixel;
        }
        
        @Override
        public String toString() {
            return name;
        }
    }
}