package com.opendemo.java.jenkins.service;

import com.opendemo.java.jenkins.model.BuildInfo;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.concurrent.atomic.AtomicLong;

public class BuildService {

    private static final Logger logger = LoggerFactory.getLogger(BuildService.class);

    private final List<BuildInfo> buildHistory = new ArrayList<>();
    private final AtomicLong buildIdGenerator = new AtomicLong(1);

    public BuildInfo startBuild(String projectName, String branch) {
        String buildId = "BUILD-" + buildIdGenerator.getAndIncrement();
        BuildInfo build = new BuildInfo(buildId, projectName, branch);
        buildHistory.add(build);
        logger.info("启动构建: {} ({})", buildId, branch);
        return build;
    }

    public void executeStage(String buildId, String stageName, String description) {
        BuildInfo build = findBuild(buildId);
        BuildInfo.StageInfo stage = new BuildInfo.StageInfo(stageName, description);
        build.addStage(stage);
        logger.info("执行阶段 [{}] - {}", stageName, description);
    }

    public void completeBuild(String buildId) {
        BuildInfo build = findBuild(buildId);
        build.setStatus("SUCCESS");
        build.setEndTime(java.time.LocalDateTime.now());
        logger.info("构建完成: {}", buildId);
    }

    public void failBuild(String buildId, String reason) {
        BuildInfo build = findBuild(buildId);
        build.setStatus("FAILURE");
        build.setEndTime(java.time.LocalDateTime.now());
        logger.error("构建失败: {} - 原因: {}", buildId, reason);
    }

    public BuildInfo getBuild(String buildId) {
        return findBuild(buildId);
    }

    public List<BuildInfo> getBuildHistory() {
        return Collections.unmodifiableList(buildHistory);
    }

    private BuildInfo findBuild(String buildId) {
        return buildHistory.stream()
                .filter(b -> b.getBuildId().equals(buildId))
                .findFirst()
                .orElseThrow(() -> new NoSuchElementException("构建不存在: " + buildId));
    }
}
