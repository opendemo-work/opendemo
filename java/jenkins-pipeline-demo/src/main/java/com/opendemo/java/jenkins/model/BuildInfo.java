package com.opendemo.java.jenkins.model;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

public class BuildInfo {

    private final String buildId;
    private final String projectName;
    private final String branch;
    private String status;
    private LocalDateTime startTime;
    private LocalDateTime endTime;
    private final List<StageInfo> stages;

    public BuildInfo(String buildId, String projectName, String branch) {
        this.buildId = buildId;
        this.projectName = projectName;
        this.branch = branch;
        this.status = "RUNNING";
        this.startTime = LocalDateTime.now();
        this.stages = new ArrayList<>();
    }

    public String getBuildId() { return buildId; }
    public String getProjectName() { return projectName; }
    public String getBranch() { return branch; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    public LocalDateTime getStartTime() { return startTime; }
    public LocalDateTime getEndTime() { return endTime; }
    public void setEndTime(LocalDateTime endTime) { this.endTime = endTime; }
    public List<StageInfo> getStages() { return stages; }

    public void addStage(StageInfo stage) {
        stages.add(stage);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        BuildInfo buildInfo = (BuildInfo) o;
        return Objects.equals(buildId, buildInfo.buildId);
    }

    @Override
    public int hashCode() {
        return Objects.hash(buildId);
    }

    @Override
    public String toString() {
        return "BuildInfo{buildId='" + buildId + "', project='" + projectName + "', branch='" + branch + "', status='" + status + "', stages=" + stages.size() + "}";
    }

    public static class StageInfo {
        private final String name;
        private final String description;
        private String status;
        private final LocalDateTime startTime;

        public StageInfo(String name, String description) {
            this.name = name;
            this.description = description;
            this.status = "SUCCESS";
            this.startTime = LocalDateTime.now();
        }

        public String getName() { return name; }
        public String getDescription() { return description; }
        public String getStatus() { return status; }
        public void setStatus(String status) { this.status = status; }
        public LocalDateTime getStartTime() { return startTime; }

        @Override
        public String toString() {
            return name + "(" + status + ")";
        }
    }
}
