package com.example.demo;

import com.example.demo.entity.*;
import com.example.demo.repository.DepartmentRepository;
import com.example.demo.repository.EmployeeRepository;
import com.example.demo.repository.ProjectRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
class HibernateMappingDemoApplicationTest {

    @Autowired
    private DepartmentRepository departmentRepository;

    @Autowired
    private EmployeeRepository employeeRepository;

    @Autowired
    private ProjectRepository projectRepository;

    @Test
    void contextLoads() {
    }

    @Test
    void testOneToManyMapping() {
        Department dept = new Department("技术部");
        Employee emp1 = new Employee("张三", "开发工程师");
        Employee emp2 = new Employee("李四", "测试工程师");
        dept.addEmployee(emp1);
        dept.addEmployee(emp2);
        departmentRepository.save(dept);

        Department found = departmentRepository.findById(dept.getId()).orElse(null);
        assertNotNull(found);
        assertEquals("技术部", found.getName());
        assertEquals(2, found.getEmployees().size());
    }

    @Test
    void testManyToOneMapping() {
        Department dept = new Department("市场部");
        departmentRepository.save(dept);
        Employee emp = new Employee("王五", "市场专员");
        emp.setDepartment(dept);
        employeeRepository.save(emp);

        Employee found = employeeRepository.findById(emp.getId()).orElse(null);
        assertNotNull(found);
        assertNotNull(found.getDepartment());
        assertEquals("市场部", found.getDepartment().getName());
    }

    @Test
    void testManyToManyMapping() {
        Employee emp = new Employee("赵六", "架构师");
        Project proj = new Project("核心系统", "核心业务系统重构");
        employeeRepository.save(emp);
        projectRepository.save(proj);

        emp.addProject(proj);
        employeeRepository.save(emp);

        Employee found = employeeRepository.findById(emp.getId()).orElse(null);
        assertNotNull(found);
        assertEquals(1, found.getProjects().size());
    }

    @Test
    void testEmbeddedAddress() {
        Department dept = new Department("行政部");
        departmentRepository.save(dept);
        Employee emp = new Employee("钱七", "行政助理");
        emp.setAddress(new Address("中关村大街1号", "北京", "100080"));
        emp.setDepartment(dept);
        employeeRepository.save(emp);

        Employee found = employeeRepository.findById(emp.getId()).orElse(null);
        assertNotNull(found);
        assertNotNull(found.getAddress());
        assertEquals("北京", found.getAddress().getCity());
        assertEquals("100080", found.getAddress().getZipCode());
    }

    @Test
    void testCascadeRemove() {
        Department dept = new Department("财务部");
        Employee emp = new Employee("孙八", "会计");
        dept.addEmployee(emp);
        departmentRepository.save(dept);
        Long deptId = dept.getId();
        Long empId = emp.getId();

        departmentRepository.deleteById(deptId);
        assertFalse(departmentRepository.findById(deptId).isPresent());
        assertFalse(employeeRepository.findById(empId).isPresent());
    }

    @Test
    void testFindEmployeesByDepartment() {
        Department dept = new Department("人事部");
        departmentRepository.save(dept);
        Employee emp = new Employee("周九", "HR");
        emp.setDepartment(dept);
        employeeRepository.save(emp);

        List<Employee> employees = employeeRepository.findByDepartmentId(dept.getId());
        assertFalse(employees.isEmpty());
        assertEquals("周九", employees.get(0).getName());
    }
}
