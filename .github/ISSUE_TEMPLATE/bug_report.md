name: Bug Report
description: 报告一个 Bug
title: "[Bug] "
labels: ["bug"]
assignees: []

body:
  - type: markdown
    attributes:
      value: |
        ## Bug 描述
        请简要描述您遇到的问题。

  - type: textarea
    id: description
    attributes:
      label: 问题描述
      description: 详细描述您遇到的问题，包括复现步骤
      placeholder: |
        1. 执行的操作
        2. 预期结果
        3. 实际结果
    validations:
      required: true

  - type: input
    id: environment
    attributes:
      label: 环境信息
      description: 操作系统、Python/Node/Java 版本等
      placeholder: macOS 14.4, Python 3.11, Node.js 20
    validations:
      required: false

  - type: textarea
    id: logs
    attributes:
      label: 相关日志
      description: 如果有错误日志，请粘贴在此
      placeholder: 将日志粘贴在这里...
    validations:
      required: false

  - type: checkboxes
    id: checklist
    attributes:
      label: 检查清单
      options:
        - label: 我已确认这不是已知问题
          required: false
        - label: 我已查看文档但未找到解决方案
          required: false