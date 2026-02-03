package com.opendemo.java.encapsulation;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.time.LocalDate;
import java.util.Collections;
import java.util.List;
import java.util.ArrayList;
import java.util.Objects;

/**
 * ImmutablePerson不可变人类 - 演示不可变对象的封装设计
 * 展示如何创建线程安全的不可变对象
 */
public final class ImmutablePerson {
    private static final Logger logger = LoggerFactory.getLogger(ImmutablePerson.class);
    
    // 所有字段都是final的 - 确保不可变性
    private final String name;
    private final int age;
    private final LocalDate birthDate;
    private final List<String> hobbies;
    private final Address address;
    
    // 私有构造方法 - 控制对象创建
    private ImmutablePerson(Builder builder) {
        this.name = builder.name;
        this.age = builder.age;
        this.birthDate = builder.birthDate;
        // 创建防御性拷贝 - 防止外部修改
        this.hobbies = Collections.unmodifiableList(new ArrayList<>(builder.hobbies));
        this.address = builder.address == null ? null : builder.address.copy();
        
        logger.info("创建不可变Person对象: {}", name);
    }
    
    // Getter方法 - 只提供读取访问
    public String getName() {
        return name;
    }
    
    public int getAge() {
        return age;
    }
    
    public LocalDate getBirthDate() {
        return birthDate;
    }
    
    // 返回防御性拷贝 - 防止外部修改内部状态
    public List<String> getHobbies() {
        return new ArrayList<>(hobbies);
    }
    
    public Address getAddress() {
        return address == null ? null : address.copy();
    }
    
    // 业务方法
    public boolean isAdult() {
        return age >= 18;
    }
    
    public int getDaysUntilNextBirthday() {
        if (birthDate == null) return -1;
        
        LocalDate today = LocalDate.now();
        LocalDate nextBirthday = birthDate.withYear(today.getYear());
        
        if (nextBirthday.isBefore(today)) {
            nextBirthday = nextBirthday.plusYears(1);
        }
        
        return (int) java.time.temporal.ChronoUnit.DAYS.between(today, nextBirthday);
    }
    
    public ImmutablePerson withName(String newName) {
        if (newName == null || newName.trim().isEmpty()) {
            throw new IllegalArgumentException("姓名不能为空");
        }
        return new Builder()
            .setName(newName)
            .setAge(this.age)
            .setBirthDate(this.birthDate)
            .setHobbies(this.hobbies)
            .setAddress(this.address)
            .build();
    }
    
    public ImmutablePerson withAge(int newAge) {
        if (newAge < 0) {
            throw new IllegalArgumentException("年龄不能为负数");
        }
        return new Builder()
            .setName(this.name)
            .setAge(newAge)
            .setBirthDate(this.birthDate)
            .setHobbies(this.hobbies)
            .setAddress(this.address)
            .build();
    }
    
    // 重写Object方法
    @Override
    public String toString() {
        return String.format("ImmutablePerson{name='%s', age=%d, birthDate=%s, hobbies=%s, address=%s}", 
                           name, age, birthDate, hobbies, address);
    }
    
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        ImmutablePerson that = (ImmutablePerson) obj;
        return age == that.age &&
               Objects.equals(name, that.name) &&
               Objects.equals(birthDate, that.birthDate) &&
               Objects.equals(hobbies, that.hobbies) &&
               Objects.equals(address, that.address);
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(name, age, birthDate, hobbies, address);
    }
    
    // 静态工厂方法
    public static ImmutablePerson create(String name, int age) {
        return new Builder()
            .setName(name)
            .setAge(age)
            .build();
    }
    
    public static ImmutablePerson createWithDetails(String name, int age, LocalDate birthDate, 
                                                   List<String> hobbies, Address address) {
        return new Builder()
            .setName(name)
            .setAge(age)
            .setBirthDate(birthDate)
            .setHobbies(hobbies)
            .setAddress(address)
            .build();
    }
    
    // Builder构建器类
    public static class Builder {
        private String name;
        private int age;
        private LocalDate birthDate;
        private List<String> hobbies = new ArrayList<>();
        private Address address;
        
        public Builder setName(String name) {
            if (name == null || name.trim().isEmpty()) {
                throw new IllegalArgumentException("姓名不能为空");
            }
            this.name = name.trim();
            return this;
        }
        
        public Builder setAge(int age) {
            if (age < 0) {
                throw new IllegalArgumentException("年龄不能为负数");
            }
            this.age = age;
            return this;
        }
        
        public Builder setBirthDate(LocalDate birthDate) {
            this.birthDate = birthDate;
            return this;
        }
        
        public Builder setHobbies(List<String> hobbies) {
            this.hobbies.clear();
            if (hobbies != null) {
                this.hobbies.addAll(hobbies);
            }
            return this;
        }
        
        public Builder addHobby(String hobby) {
            if (hobby != null && !hobby.trim().isEmpty()) {
                this.hobbies.add(hobby.trim());
            }
            return this;
        }
        
        public Builder setAddress(Address address) {
            this.address = address;
            return this;
        }
        
        public ImmutablePerson build() {
            if (name == null || name.isEmpty()) {
                throw new IllegalStateException("必须设置姓名");
            }
            return new ImmutablePerson(this);
        }
    }
    
    // 内部Address类 - 同样是不可变的
    public static final class Address {
        private final String street;
        private final String city;
        private final String postalCode;
        private final String country;
        
        public Address(String street, String city, String postalCode, String country) {
            this.street = street;
            this.city = city;
            this.postalCode = postalCode;
            this.country = country;
        }
        
        // Getter方法
        public String getStreet() { return street; }
        public String getCity() { return city; }
        public String getPostalCode() { return postalCode; }
        public String getCountry() { return country; }
        
        // 创建拷贝
        public Address copy() {
            return new Address(street, city, postalCode, country);
        }
        
        @Override
        public String toString() {
            return String.format("Address{street='%s', city='%s', postalCode='%s', country='%s'}", 
                               street, city, postalCode, country);
        }
        
        @Override
        public boolean equals(Object obj) {
            if (this == obj) return true;
            if (obj == null || getClass() != obj.getClass()) return false;
            Address address = (Address) obj;
            return Objects.equals(street, address.street) &&
                   Objects.equals(city, address.city) &&
                   Objects.equals(postalCode, address.postalCode) &&
                   Objects.equals(country, address.country);
        }
        
        @Override
        public int hashCode() {
            return Objects.hash(street, city, postalCode, country);
        }
    }
}