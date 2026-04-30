package com.opendemo.java.refactoring.after;

public class IntroduceParameterObjectAfter {
    public void createReport(CustomerInfo customer) {
        System.out.println("Report for: " + customer.getFullName());
        System.out.println("Age: " + customer.getAge());
        System.out.println("Address: " + customer.getAddress());
        System.out.println("Contact: " + customer.getPhone() + " / " + customer.getEmail());
    }

    public boolean isValidCustomer(CustomerInfo customer) {
        return customer.getFirstName() != null && customer.getLastName() != null
                && customer.getAge() >= 18 && customer.getCity() != null
                && customer.getPhone() != null;
    }

    public String getGreeting(CustomerInfo customer) {
        return "Hello, " + customer.getFullName() + "!";
    }
}
