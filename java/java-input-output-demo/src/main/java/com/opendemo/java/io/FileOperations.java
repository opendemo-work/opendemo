package com.opendemo.java.io;

import java.io.IOException;
import java.nio.file.*;
import java.nio.file.attribute.BasicFileAttributes;

public class FileOperations {

    public static boolean exists(String filePath) {
        return Files.exists(Paths.get(filePath));
    }

    public static Path copy(String source, String target) throws IOException {
        Path sourcePath = Paths.get(source);
        Path targetPath = Paths.get(target);
        return Files.copy(sourcePath, targetPath, StandardCopyOption.REPLACE_EXISTING);
    }

    public static Path move(String source, String target) throws IOException {
        Path sourcePath = Paths.get(source);
        Path targetPath = Paths.get(target);
        return Files.move(sourcePath, targetPath, StandardCopyOption.REPLACE_EXISTING);
    }

    public static boolean delete(String filePath) throws IOException {
        return Files.deleteIfExists(Paths.get(filePath));
    }

    public static long size(String filePath) throws IOException {
        return Files.size(Paths.get(filePath));
    }

    public static Path createTempFile(String prefix, String suffix) throws IOException {
        return Files.createTempFile(prefix, suffix);
    }

    public static Path createTempDir(String prefix) throws IOException {
        return Files.createTempDirectory(prefix);
    }

    public static void createFile(String filePath) throws IOException {
        Files.createFile(Paths.get(filePath));
    }

    public static void createDirectory(String dirPath) throws IOException {
        Files.createDirectories(Paths.get(dirPath));
    }

    public static void deleteRecursively(String dirPath) throws IOException {
        Path path = Paths.get(dirPath);
        Files.walkFileTree(path, new SimpleFileVisitor<Path>() {
            @Override
            public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) throws IOException {
                Files.delete(file);
                return FileVisitResult.CONTINUE;
            }

            @Override
            public FileVisitResult postVisitDirectory(Path dir, IOException exc) throws IOException {
                Files.delete(dir);
                return FileVisitResult.CONTINUE;
            }
        });
    }
}
