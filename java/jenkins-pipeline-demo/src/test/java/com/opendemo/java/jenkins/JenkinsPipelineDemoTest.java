package com.opendemo.java.jenkins;

import com.opendemo.java.jenkins.model.BuildInfo;
import com.opendemo.java.jenkins.service.BuildService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.NoSuchElementException;

import static org.junit.jupiter.api.Assertions.*;

class JenkinsPipelineDemoTest {

    private BuildService buildService;

    @BeforeEach
    void setUp() {
        buildService = new BuildService();
    }

    @Test
    void testMainRunsSuccessfully() {
        assertDoesNotThrow(() -> JenkinsPipelineDemo.main(new String[]{}));
    }

    @Test
    void testStartBuild() {
        BuildInfo build = buildService.startBuild("test-project", "main");
        assertNotNull(build.getBuildId());
        assertEquals("test-project", build.getProjectName());
        assertEquals("main", build.getBranch());
        assertEquals("RUNNING", build.getStatus());
    }

    @Test
    void testExecuteStage() {
        BuildInfo build = buildService.startBuild("test-project", "main");
        buildService.executeStage(build.getBuildId(), "Build", "编译项目");
        assertEquals(1, build.getStages().size());
        assertEquals("Build", build.getStages().get(0).getName());
        assertEquals("SUCCESS", build.getStages().get(0).getStatus());
    }

    @Test
    void testMultipleStages() {
        BuildInfo build = buildService.startBuild("test-project", "dev");
        buildService.executeStage(build.getBuildId(), "Checkout", "检出代码");
        buildService.executeStage(build.getBuildId(), "Build", "编译项目");
        buildService.executeStage(build.getBuildId(), "Test", "执行测试");
        assertEquals(3, build.getStages().size());
    }

    @Test
    void testCompleteBuild() {
        BuildInfo build = buildService.startBuild("test-project", "main");
        buildService.executeStage(build.getBuildId(), "Build", "编译");
        buildService.completeBuild(build.getBuildId());
        assertEquals("SUCCESS", build.getStatus());
        assertNotNull(build.getEndTime());
    }

    @Test
    void testFailBuild() {
        BuildInfo build = buildService.startBuild("test-project", "main");
        buildService.failBuild(build.getBuildId(), "编译错误");
        assertEquals("FAILURE", build.getStatus());
        assertNotNull(build.getEndTime());
    }

    @Test
    void testGetBuildNotFound() {
        assertThrows(NoSuchElementException.class, () -> buildService.getBuild("BUILD-999"));
    }

    @Test
    void testBuildHistory() {
        buildService.startBuild("project-1", "main");
        buildService.startBuild("project-2", "dev");
        List<BuildInfo> history = buildService.getBuildHistory();
        assertEquals(2, history.size());
    }
}
