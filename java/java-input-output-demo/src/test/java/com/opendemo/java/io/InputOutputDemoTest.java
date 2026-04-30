package com.opendemo.java.io;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;
import static org.junit.jupiter.api.Assertions.*;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;

class InputOutputDemoTest {

    @TempDir
    Path tempDir;

    @Test
    void testFileReadWrite() throws IOException {
        Path testFile = tempDir.resolve("test.txt");
        String content = "Hello, Java IO!";

        Files.write(testFile, content.getBytes(StandardCharsets.UTF_8));
        assertTrue(Files.exists(testFile));

        String readBack = new String(Files.readAllBytes(testFile), StandardCharsets.UTF_8);
        assertEquals(content, readBack);
    }

    @Test
    void testBufferedWriteAndRead() throws IOException {
        Path testFile = tempDir.resolve("buffered.txt");

        try (BufferedWriter writer = Files.newBufferedWriter(testFile, StandardCharsets.UTF_8)) {
            writer.write("第一行");
            writer.newLine();
            writer.write("第二行");
        }

        try (BufferedReader reader = Files.newBufferedReader(testFile, StandardCharsets.UTF_8)) {
            assertEquals("第一行", reader.readLine());
            assertEquals("第二行", reader.readLine());
            assertNull(reader.readLine());
        }
    }

    @Test
    void testFileCopy() throws IOException {
        Path source = tempDir.resolve("source.txt");
        Path target = tempDir.resolve("target.txt");

        Files.write(source, "copy test content".getBytes(StandardCharsets.UTF_8));
        FileOperations.copy(source.toString(), target.toString());

        assertTrue(Files.exists(target));
        assertEquals(new String(Files.readAllBytes(source), StandardCharsets.UTF_8),
                new String(Files.readAllBytes(target), StandardCharsets.UTF_8));
    }

    @Test
    void testFileMove() throws IOException {
        Path source = tempDir.resolve("move-source.txt");
        Path target = tempDir.resolve("move-target.txt");

        Files.write(source, "move test content".getBytes(StandardCharsets.UTF_8));
        FileOperations.move(source.toString(), target.toString());

        assertFalse(Files.exists(source));
        assertTrue(Files.exists(target));
        assertEquals("move test content", new String(Files.readAllBytes(target), StandardCharsets.UTF_8));
    }

    @Test
    void testFileDelete() throws IOException {
        Path file = tempDir.resolve("to-delete.txt");
        Files.write(file, "delete me".getBytes(StandardCharsets.UTF_8));
        assertTrue(Files.exists(file));

        FileOperations.delete(file.toString());
        assertFalse(Files.exists(file));
    }

    @Test
    void testFileExists() throws IOException {
        Path existing = tempDir.resolve("existing.txt");
        Path nonExisting = tempDir.resolve("non-existing.txt");

        Files.write(existing, "data".getBytes(StandardCharsets.UTF_8));

        assertTrue(FileOperations.exists(existing.toString()));
        assertFalse(FileOperations.exists(nonExisting.toString()));
    }

    @Test
    void testFileSize() throws IOException {
        Path file = tempDir.resolve("sized.txt");
        String content = "1234567890";
        Files.write(file, content.getBytes(StandardCharsets.UTF_8));

        assertEquals(10, FileOperations.size(file.toString()));
    }

    @Test
    void testStreamReaderWriter() throws IOException {
        Path file = tempDir.resolve("encoding-test.txt");
        String chineseText = "你好，世界！";

        StreamReaderWriter.writeFileWithEncoding(file, chineseText, StandardCharsets.UTF_8);
        String readBack = StreamReaderWriter.readFileWithEncoding(file, StandardCharsets.UTF_8);

        assertEquals(chineseText + "\n", readBack);
    }

    @Test
    void testEncodingConversion() {
        String text = "Hello, 世界!";
        byte[] utf8Bytes = StreamReaderWriter.convertStringToBytes(text, StandardCharsets.UTF_8);
        String restored = StreamReaderWriter.convertBytesToString(utf8Bytes, StandardCharsets.UTF_8);

        assertEquals(text, restored);
        assertTrue(utf8Bytes.length > text.length());
    }

    @Test
    void testObjectSerialization() throws IOException, ClassNotFoundException {
        Path serFile = tempDir.resolve("person.ser");
        ObjectSerializationDemo.Person original = new ObjectSerializationDemo.Person("张三", 25, "secret123");

        ObjectSerializationDemo.serialize(serFile, original);
        assertTrue(Files.exists(serFile));

        ObjectSerializationDemo.Person restored = ObjectSerializationDemo.deserialize(serFile);
        assertEquals("张三", restored.getName());
        assertEquals(25, restored.getAge());
        assertNull(restored.getPassword());
    }

    @Test
    void testTransientFieldIsNull() throws IOException, ClassNotFoundException {
        Path serFile = tempDir.resolve("transient.ser");
        ObjectSerializationDemo.Person person = new ObjectSerializationDemo.Person("Test", 30, "password");

        ObjectSerializationDemo.serialize(serFile, person);
        ObjectSerializationDemo.Person restored = ObjectSerializationDemo.deserialize(serFile);

        assertNull(restored.getPassword());
        assertEquals("Test", restored.getName());
        assertEquals(30, restored.getAge());
    }

    @Test
    void testNIOFileCopy() throws IOException {
        Path source = tempDir.resolve("nio-source.txt");
        Path target = tempDir.resolve("nio-target.txt");

        String content = "NIO copy test";
        Files.write(source, content.getBytes(StandardCharsets.UTF_8));

        java.nio.file.Files.copy(source, target, java.nio.file.StandardCopyOption.REPLACE_EXISTING);

        assertTrue(Files.exists(target));
        assertEquals(content, new String(Files.readAllBytes(target), StandardCharsets.UTF_8));
    }

    @Test
    void testInputOutputDemoHelperMethods() throws IOException {
        Path file = tempDir.resolve("helper.txt");
        java.util.List<String> lines = java.util.List.of("line1", "line2", "line3");

        InputOutputDemo.writeAllLines(file.toString(), lines);
        java.util.List<String> readLines = InputOutputDemo.readAllLines(file.toString());

        assertEquals(lines, readLines);
    }

    @Test
    void testCreateTempFile() throws IOException {
        Path tempFile = FileOperations.createTempFile("test-", ".txt");
        assertTrue(Files.exists(tempFile));
        assertTrue(tempFile.getFileName().toString().startsWith("test-"));
        assertTrue(tempFile.getFileName().toString().endsWith(".txt"));
        Files.deleteIfExists(tempFile);
    }

    @Test
    void testCreateDirectory() throws IOException {
        Path newDir = tempDir.resolve("new-dir");
        FileOperations.createDirectory(newDir.toString());
        assertTrue(Files.isDirectory(newDir));
    }
}
