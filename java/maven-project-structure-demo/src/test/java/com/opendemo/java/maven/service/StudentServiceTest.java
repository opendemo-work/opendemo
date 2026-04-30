package com.opendemo.java.maven.service;

import com.opendemo.java.maven.exception.StudentNotFoundException;
import com.opendemo.java.maven.model.Student;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class StudentServiceTest {

    private StudentService studentService;

    @BeforeEach
    void setUp() {
        studentService = new StudentService();
        studentService.addStudent(new Student(1, "张三", 20, "计算机科学"));
        studentService.addStudent(new Student(2, "李四", 21, "软件工程"));
        studentService.addStudent(new Student(3, "王五", 22, "计算机科学"));
    }

    @Test
    void testAddStudent() {
        studentService.addStudent(new Student(4, "赵六", 23, "人工智能"));
        assertEquals(4, studentService.getAllStudents().size());
    }

    @Test
    void testGetStudentById() {
        Student student = studentService.getStudentById(1);
        assertEquals("张三", student.getName());
        assertEquals(20, student.getAge());
    }

    @Test
    void testGetStudentByIdNotFound() {
        assertThrows(StudentNotFoundException.class, () -> studentService.getStudentById(999));
    }

    @Test
    void testGetAllStudents() {
        List<Student> students = studentService.getAllStudents();
        assertEquals(3, students.size());
    }

    @Test
    void testRemoveStudent() {
        assertTrue(studentService.removeStudent(1));
        assertEquals(2, studentService.getAllStudents().size());
    }

    @Test
    void testRemoveStudentNotFound() {
        assertFalse(studentService.removeStudent(999));
    }

    @Test
    void testUpdateStudent() {
        Student updated = new Student(1, "张三丰", 25, "网络安全");
        Student result = studentService.updateStudent(updated);
        assertEquals("张三丰", result.getName());
        assertEquals(25, result.getAge());
    }

    @Test
    void testUpdateStudentNotFound() {
        Student updated = new Student(999, "不存在", 0, "无");
        assertThrows(StudentNotFoundException.class, () -> studentService.updateStudent(updated));
    }

    @Test
    void testGetAverageAge() {
        double avgAge = studentService.getAverageAge();
        assertEquals(21.0, avgAge, 0.01);
    }

    @Test
    void testGetAverageAgeEmptyList() {
        StudentService emptyService = new StudentService();
        assertEquals(0.0, emptyService.getAverageAge());
    }

    @Test
    void testGetStudentsByMajor() {
        List<Student> csStudents = studentService.getStudentsByMajor("计算机科学");
        assertEquals(2, csStudents.size());
    }
}
