package com.opendemo.java.refactoring.before;

import java.time.LocalDate;
import java.time.Month;

public class DecomposeConditionalBefore {
    private LocalDate date;
    private double rate;

    public DecomposeConditionalBefore(LocalDate date, double rate) {
        this.date = date;
        this.rate = rate;
    }

    public double calculateCharge(double quantity) {
        if (date.getMonthValue() >= 6 && date.getMonthValue() <= 8) {
            return quantity * rate * 1.5;
        } else if (date.getMonthValue() >= 11 || date.getMonthValue() <= 2) {
            return quantity * rate * 1.2;
        } else {
            return quantity * rate;
        }
    }

    public String getSeason() {
        if (date.getMonthValue() >= 6 && date.getMonthValue() <= 8) {
            return "Summer";
        } else if (date.getMonthValue() >= 11 || date.getMonthValue() <= 2) {
            return "Winter";
        } else {
            return "Off-season";
        }
    }
}
