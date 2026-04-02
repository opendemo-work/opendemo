// ESLint 配置
// 安装: npm install --save-dev eslint prettier eslint-config-prettier eslint-plugin-node
// 使用: npx eslint nodejs/

module.exports = {
  root: true,
  env: {
    node: true,
    es2022: true,
    jest: true,
  },
  extends: [
    'eslint:recommended',
    'plugin:node/recommended',
    'prettier',
  ],
  plugins: [
    'node',
  ],
  parserOptions: {
    ecmaVersion: 2022,
    sourceType: 'module',
  },
  rules: {
    // 错误预防
    'no-console': 'off',  // 允许 console，因为这是 CLI 工具
    'no-unused-vars': ['error', { 
      argsIgnorePattern: '^_',
      varsIgnorePattern: '^_',
    }],
    'no-undef': 'error',
    'no-var': 'error',
    'prefer-const': 'error',
    
    // 代码风格
    'indent': ['error', 2],
    'quotes': ['error', 'single', { avoidEscape: true }],
    'semi': ['error', 'always'],
    'comma-dangle': ['error', 'always-multiline'],
    'max-len': ['warn', { 
      code: 120,
      ignoreUrls: true,
      ignoreStrings: true,
      ignoreTemplateLiterals: true,
    }],
    
    // Node.js 特定
    'node/no-unpublished-require': 'off',
    'node/no-missing-require': 'error',
    'node/no-deprecated-api': 'warn',
    'node/exports-style': ['error', 'module.exports'],
    'node/file-extension-in-import': ['error', 'always'],
    'node/prefer-global/buffer': 'error',
    'node/prefer-global/console': 'error',
    'node/prefer-global/process': 'error',
    'node/prefer-global/url': 'error',
    'node/prefer-global/url-search-params': 'error',
    
    // 最佳实践
    'eqeqeq': ['error', 'always'],
    'curly': ['error', 'all'],
    'no-throw-literal': 'error',
    'prefer-promise-reject-errors': 'error',
    'no-return-await': 'error',
    'require-await': 'error',
  },
  overrides: [
    {
      // 测试文件特殊规则
      files: ['**/*.test.js', '**/*.spec.js'],
      rules: {
        'no-undef': 'off',  // jest 全局变量
        'node/no-unpublished-require': 'off',
      },
    },
    {
      // 配置文件特殊规则
      files: ['*.config.js', '.eslintrc.js'],
      rules: {
        'node/no-unpublished-require': 'off',
      },
    },
  ],
  ignorePatterns: [
    'node_modules/',
    'coverage/',
    'dist/',
    'build/',
    '*.min.js',
  ],
};
