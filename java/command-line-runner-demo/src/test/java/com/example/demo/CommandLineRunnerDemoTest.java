package com.example.demo;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class CommandLineRunnerDemoTest {

    @Test
    void testStartupRunnerCreation() {
        StartupRunner runner = new StartupRunner();
        assertNotNull(runner);
    }

    @Test
    void testStartupRunnerExecution() {
        StartupRunner runner = new StartupRunner();
        assertDoesNotThrow(() -> runner.run("--env=dev", "input.txt"));
    }

    @Test
    void testStartupRunnerWithNoArgs() {
        StartupRunner runner = new StartupRunner();
        assertDoesNotThrow(() -> runner.run());
    }

    @Test
    void testTaskRunnerCreation() {
        TaskRunner runner = new TaskRunner();
        assertNotNull(runner);
    }

    @Test
    void testTaskRunnerExecution() {
        TaskRunner runner = new TaskRunner();
        assertDoesNotThrow(() -> runner.run("--health-check"));
    }

    @Test
    void testTaskRunnerWithoutHealthCheck() {
        TaskRunner runner = new TaskRunner();
        assertDoesNotThrow(() -> runner.run("--normal"));
    }

    @Test
    void testTaskRunnerWithNoArgs() {
        TaskRunner runner = new TaskRunner();
        assertDoesNotThrow(() -> runner.run());
    }

    @Test
    void testSystemProperties() {
        assertNotNull(System.getProperty("java.version"));
        assertNotNull(System.getProperty("os.name"));
        assertNotNull(System.getProperty("user.dir"));
    }

    @Test
    void testRuntimeInfo() {
        Runtime runtime = Runtime.getRuntime();
        assertTrue(runtime.availableProcessors() > 0);
        assertTrue(runtime.totalMemory() > 0);
        assertTrue(runtime.maxMemory() > 0);
    }

    @Test
    void testArgParsing() {
        String[] args = {"--env=prod", "--debug", "input.txt"};
        assertEquals(3, args.length);
        assertTrue(args[0].startsWith("--"));
        assertEquals("input.txt", args[2]);
    }
}
