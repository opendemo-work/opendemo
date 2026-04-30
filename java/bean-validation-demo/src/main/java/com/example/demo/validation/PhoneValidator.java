package com.example.demo.validation;

import javax.validation.ConstraintValidator;
import javax.validation.ConstraintValidatorContext;

import java.util.regex.Pattern;

public class PhoneValidator implements ConstraintValidator<Phone, String> {

    private static final Pattern PHONE_PATTERN = Pattern.compile("^1[3-9]\\d{9}$");

    @Override
    public void initialize(Phone annotation) {
    }

    @Override
    public boolean isValid(String phone, ConstraintValidatorContext context) {
        if (phone == null || phone.trim().isEmpty()) {
            return true;
        }
        return PHONE_PATTERN.matcher(phone).matches();
    }
}
