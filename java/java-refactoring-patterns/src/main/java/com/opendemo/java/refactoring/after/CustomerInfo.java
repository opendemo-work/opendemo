package com.opendemo.java.refactoring.after;

public class CustomerInfo {
    private final String firstName;
    private final String lastName;
    private final int age;
    private final String street;
    private final String city;
    private final String zipCode;
    private final String phone;
    private final String email;

    public CustomerInfo(String firstName, String lastName, int age,
                        String street, String city, String zipCode,
                        String phone, String email) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.age = age;
        this.street = street;
        this.city = city;
        this.zipCode = zipCode;
        this.phone = phone;
        this.email = email;
    }

    public String getFirstName() { return firstName; }
    public String getLastName() { return lastName; }
    public int getAge() { return age; }
    public String getStreet() { return street; }
    public String getCity() { return city; }
    public String getZipCode() { return zipCode; }
    public String getPhone() { return phone; }
    public String getEmail() { return email; }
    public String getFullName() { return firstName + " " + lastName; }
    public String getAddress() { return street + ", " + city + " " + zipCode; }
}
