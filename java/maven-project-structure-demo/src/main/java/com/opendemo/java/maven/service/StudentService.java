package com.opendemo.java.maven.service;

import com.opendemo.java.maven.exception.StudentNotFoundException;
import com.opendemo.java.maven.model.Student;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Optional;

public class StudentService {

    private final List<Student> students = new ArrayList<>();

    public void addStudent(Student student) {
        students.add(student);
    }

    public Student getStudentById(int id) {
        return students.stream()
                .filter(s -> s.getId() == id)
                .findFirst()
                .orElseThrow(() -> new StudentNotFoundException("未找到ID为 " + id + " 的学生"));
    }

    public List<Student> getAllStudents() {
        return Collections.unmodifiableList(students);
    }

    public boolean removeStudent(int id) {
        return students.removeIf(s -> s.getId() == id);
    }

    public Student updateStudent(Student updated) {
        Optional<Student> existing = students.stream()
                .filter(s -> s.getId() == updated.getId())
                .findFirst();

        if (existing.isPresent()) {
            Student s = existing.get();
            s.setName(updated.getName());
            s.setAge(updated.getAge());
            s.setMajor(updated.getMajor());
            return s;
        }
        throw new StudentNotFoundException("未找到ID为 " + updated.getId() + " 的学生");
    }

    public double getAverageAge() {
        return students.stream()
                .mapToInt(Student::getAge)
                .average()
                .orElse(0.0);
    }

    public List<Student> getStudentsByMajor(String major) {
        List<Student> result = new ArrayList<>();
        for (Student s : students) {
            if (s.getMajor().equals(major)) {
                result.add(s);
            }
        }
        return result;
    }
}
