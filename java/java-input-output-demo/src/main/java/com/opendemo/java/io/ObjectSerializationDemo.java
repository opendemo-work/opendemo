package com.opendemo.java.io;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;

public class ObjectSerializationDemo {

    public static class Person implements Serializable {
        private static final long serialVersionUID = 1L;
        private String name;
        private int age;
        private transient String password;

        public Person() {
        }

        public Person(String name, int age, String password) {
            this.name = name;
            this.age = age;
            this.password = password;
        }

        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }

        public int getAge() {
            return age;
        }

        public void setAge(int age) {
            this.age = age;
        }

        public String getPassword() {
            return password;
        }

        public void setPassword(String password) {
            this.password = password;
        }

        @Override
        public String toString() {
            return "Person{name='" + name + "', age=" + age + ", password='" + password + "'}";
        }
    }

    public static void serialize(Path path, Serializable obj) throws IOException {
        try (ObjectOutputStream oos = new ObjectOutputStream(Files.newOutputStream(path))) {
            oos.writeObject(obj);
        }
    }

    @SuppressWarnings("unchecked")
    public static <T> T deserialize(Path path) throws IOException, ClassNotFoundException {
        try (ObjectInputStream ois = new ObjectInputStream(Files.newInputStream(path))) {
            return (T) ois.readObject();
        }
    }

    public static void main(String[] args) throws IOException, ClassNotFoundException {
        System.out.println("=== 对象序列化演示 ===\n");

        Path tempFile = Files.createTempFile("serial-", ".dat");

        Person original = new Person("张三", 25, "secret123");
        System.out.println("原始对象: " + original);

        serialize(tempFile, original);
        System.out.println("序列化完成，文件大小: " + Files.size(tempFile) + " bytes");

        Person restored = deserialize(tempFile);
        System.out.println("反序列化对象: " + restored);
        System.out.println("transient字段password应为null: " + (restored.getPassword() == null));

        Files.deleteIfExists(tempFile);
    }
}
