package com.example.demo.controller;

import com.example.demo.entity.Department;
import com.example.demo.entity.Employee;
import com.example.demo.entity.Project;
import com.example.demo.service.CompanyService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api")
public class CompanyController {

    private final CompanyService companyService;

    public CompanyController(CompanyService companyService) {
        this.companyService = companyService;
    }

    @PostMapping("/departments")
    public ResponseEntity<Department> createDepartment(@RequestBody Department department) {
        Department created = companyService.createDepartment(department.getName());
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }

    @GetMapping("/departments")
    public ResponseEntity<List<Department>> getAllDepartments() {
        return ResponseEntity.ok(companyService.getAllDepartments());
    }

    @GetMapping("/departments/{id}")
    public ResponseEntity<Department> getDepartment(@PathVariable Long id) {
        return companyService.getDepartmentById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping("/departments/{departmentId}/employees")
    public ResponseEntity<Employee> addEmployee(@PathVariable Long departmentId,
                                                 @RequestBody Employee employee) {
        Employee created = companyService.addEmployeeToDepartment(
                departmentId,
                employee.getName(),
                employee.getPosition(),
                employee.getAddress() != null ? employee.getAddress().getStreet() : null,
                employee.getAddress() != null ? employee.getAddress().getCity() : null,
                employee.getAddress() != null ? employee.getAddress().getZipCode() : null
        );
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }

    @GetMapping("/departments/{departmentId}/employees")
    public ResponseEntity<List<Employee>> getDepartmentEmployees(@PathVariable Long departmentId) {
        return ResponseEntity.ok(companyService.getEmployeesByDepartment(departmentId));
    }

    @PostMapping("/projects")
    public ResponseEntity<Project> createProject(@RequestBody Project project) {
        Project created = companyService.createProject(project.getName(), project.getDescription());
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }

    @GetMapping("/projects")
    public ResponseEntity<List<Project>> getAllProjects() {
        return ResponseEntity.ok(companyService.getAllProjects());
    }

    @PostMapping("/employees/{employeeId}/projects/{projectId}")
    public ResponseEntity<Void> assignProject(@PathVariable Long employeeId, @PathVariable Long projectId) {
        companyService.assignEmployeeToProject(employeeId, projectId);
        return ResponseEntity.ok().build();
    }

    @GetMapping("/employees")
    public ResponseEntity<List<Employee>> getAllEmployees() {
        return ResponseEntity.ok(companyService.getAllEmployees());
    }

    @GetMapping("/employees/{id}")
    public ResponseEntity<Employee> getEmployee(@PathVariable Long id) {
        return companyService.getEmployeeById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @DeleteMapping("/departments/{id}")
    public ResponseEntity<Void> deleteDepartment(@PathVariable Long id) {
        companyService.deleteDepartment(id);
        return ResponseEntity.noContent().build();
    }

    @DeleteMapping("/employees/{id}")
    public ResponseEntity<Void> deleteEmployee(@PathVariable Long id) {
        companyService.deleteEmployee(id);
        return ResponseEntity.noContent().build();
    }

    @DeleteMapping("/projects/{id}")
    public ResponseEntity<Void> deleteProject(@PathVariable Long id) {
        companyService.deleteProject(id);
        return ResponseEntity.noContent().build();
    }
}
