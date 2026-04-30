package com.opendemo.java.jenkins;

import com.opendemo.java.jenkins.model.BuildInfo;
import com.opendemo.java.jenkins.service.BuildService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class JenkinsPipelineDemo {

    private static final Logger logger = LoggerFactory.getLogger(JenkinsPipelineDemo.class);

    public static void main(String[] args) {
        logger.info("=== Jenkins Pipeline Demo ===");
        logger.info("演示CI/CD流水线的构建过程");
        logger.info("");

        BuildService buildService = new BuildService();

        BuildInfo build = buildService.startBuild("jenkins-pipeline-demo", "main");
        logger.info("构建启动: {}", build);

        buildService.executeStage(build.getBuildId(), "Checkout", "从Git仓库检出代码");
        buildService.executeStage(build.getBuildId(), "Build", "使用Maven编译项目");
        buildService.executeStage(build.getBuildId(), "Test", "执行JUnit单元测试");
        buildService.executeStage(build.getBuildId(), "Package", "打包为JAR文件");

        if ("main".equals(build.getBranch())) {
            buildService.executeStage(build.getBuildId(), "Deploy", "部署到生产环境");
        }

        buildService.completeBuild(build.getBuildId());
        logger.info("构建完成: {}", build);

        logger.info("");
        logger.info("--- 构建历史 ---");
        buildService.getBuildHistory().forEach(b ->
            logger.info("  构建ID: {} | 状态: {} | 阶段数: {}",
                b.getBuildId(), b.getStatus(), b.getStages().size())
        );
    }
}
