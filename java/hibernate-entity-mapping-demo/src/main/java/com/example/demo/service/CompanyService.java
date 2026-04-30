package com.example.demo.service;

import com.example.demo.entity.*;
import com.example.demo.repository.DepartmentRepository;
import com.example.demo.repository.EmployeeRepository;
import com.example.demo.repository.ProjectRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
public class CompanyService {

    private final DepartmentRepository departmentRepository;
    private final EmployeeRepository employeeRepository;
    private final ProjectRepository projectRepository;

    public CompanyService(DepartmentRepository departmentRepository,
                          EmployeeRepository employeeRepository,
                          ProjectRepository projectRepository) {
        this.departmentRepository = departmentRepository;
        this.employeeRepository = employeeRepository;
        this.projectRepository = projectRepository;
    }

    @Transactional
    public Department createDepartment(String name) {
        return departmentRepository.save(new Department(name));
    }

    public List<Department> getAllDepartments() {
        return departmentRepository.findAll();
    }

    public Optional<Department> getDepartmentById(Long id) {
        return departmentRepository.findById(id);
    }

    @Transactional
    public Employee addEmployeeToDepartment(Long departmentId, String name, String position,
                                             String street, String city, String zipCode) {
        Department department = departmentRepository.findById(departmentId)
                .orElseThrow(() -> new RuntimeException("Department not found"));
        Employee employee = new Employee(name, position);
        if (street != null || city != null || zipCode != null) {
            employee.setAddress(new Address(street, city, zipCode));
        }
        department.addEmployee(employee);
        return employeeRepository.save(employee);
    }

    @Transactional
    public Project createProject(String name, String description) {
        return projectRepository.save(new Project(name, description));
    }

    public List<Project> getAllProjects() {
        return projectRepository.findAll();
    }

    @Transactional
    public void assignEmployeeToProject(Long employeeId, Long projectId) {
        Employee employee = employeeRepository.findById(employeeId)
                .orElseThrow(() -> new RuntimeException("Employee not found"));
        Project project = projectRepository.findById(projectId)
                .orElseThrow(() -> new RuntimeException("Project not found"));
        employee.addProject(project);
        employeeRepository.save(employee);
    }

    public List<Employee> getEmployeesByDepartment(Long departmentId) {
        return employeeRepository.findByDepartmentId(departmentId);
    }

    public List<Employee> getEmployeesByProject(Long projectId) {
        return employeeRepository.findByProjectsId(projectId);
    }

    public Optional<Employee> getEmployeeById(Long id) {
        return employeeRepository.findById(id);
    }

    public List<Employee> getAllEmployees() {
        return employeeRepository.findAll();
    }

    @Transactional
    public void deleteDepartment(Long id) {
        departmentRepository.deleteById(id);
    }

    @Transactional
    public void deleteEmployee(Long id) {
        employeeRepository.deleteById(id);
    }

    @Transactional
    public void deleteProject(Long id) {
        projectRepository.deleteById(id);
    }
}
