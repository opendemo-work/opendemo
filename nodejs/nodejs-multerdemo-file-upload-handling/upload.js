/**
 * 自定义Multer上传配置
 * 支持磁盘存储、文件名重命名和类型过滤
 */
const multer = require('multer');
const path = require('path');

// 自定义存储引擎：保留扩展名并生成随机文件名
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    // 设置文件保存目录
    cb(null, 'uploads/');
  },
  filename: function (req, file, cb) {
    // 生成唯一文件名：时间戳 + 随机数 + 原始扩展名
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    cb(null, file.fieldname + '-' + uniqueSuffix + path.extname(file.originalname));
  }
});

// 文件过滤器：仅允许图像文件
function fileFilter(req, file, cb) {
  const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif'];

  if (allowedTypes.includes(file.mimetype)) {
    cb(null, true); // 接受文件
  } else {
    cb(new Error('不支持的文件类型，请上传 JPG、PNG 或 GIF'), false); // 拒绝文件
  }
}

// 创建Multer实例
const upload = multer({
  storage: storage,
  fileFilter: fileFilter,
  limits: {
    fileSize: 10 * 1024 * 1024 // 限制单个文件最大为10MB
  }
});

module.exports = upload;