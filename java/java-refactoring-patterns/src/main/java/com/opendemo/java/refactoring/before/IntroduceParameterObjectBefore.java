package com.opendemo.java.refactoring.before;

public class IntroduceParameterObjectBefore {
    public void createReport(String firstName, String lastName, int age,
                             String street, String city, String zipCode,
                             String phone, String email) {
        System.out.println("Report for: " + firstName + " " + lastName);
        System.out.println("Age: " + age);
        System.out.println("Address: " + street + ", " + city + " " + zipCode);
        System.out.println("Contact: " + phone + " / " + email);
    }

    public boolean isValidCustomer(String firstName, String lastName, int age,
                                   String street, String city, String zipCode,
                                   String phone, String email) {
        return firstName != null && lastName != null && age >= 18
                && city != null && phone != null;
    }

    public String getGreeting(String firstName, String lastName, int age,
                              String street, String city, String zipCode,
                              String phone, String email) {
        return "Hello, " + firstName + " " + lastName + "!";
    }
}
