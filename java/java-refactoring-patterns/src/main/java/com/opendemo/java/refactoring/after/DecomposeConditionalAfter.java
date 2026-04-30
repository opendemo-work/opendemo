package com.opendemo.java.refactoring.after;

import java.time.LocalDate;

public class DecomposeConditionalAfter {
    private LocalDate date;
    private double rate;

    public DecomposeConditionalAfter(LocalDate date, double rate) {
        this.date = date;
        this.rate = rate;
    }

    private boolean isSummer() {
        int month = date.getMonthValue();
        return month >= 6 && month <= 8;
    }

    private boolean isWinter() {
        int month = date.getMonthValue();
        return month >= 11 || month <= 2;
    }

    private double summerCharge(double quantity) {
        return quantity * rate * 1.5;
    }

    private double winterCharge(double quantity) {
        return quantity * rate * 1.2;
    }

    private double regularCharge(double quantity) {
        return quantity * rate;
    }

    public double calculateCharge(double quantity) {
        if (isSummer()) {
            return summerCharge(quantity);
        } else if (isWinter()) {
            return winterCharge(quantity);
        } else {
            return regularCharge(quantity);
        }
    }

    public String getSeason() {
        if (isSummer()) return "Summer";
        if (isWinter()) return "Winter";
        return "Off-season";
    }
}
