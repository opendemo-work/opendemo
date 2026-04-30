package com.opendemo.java.patterns.decorator;

public class WhipDecorator extends CoffeeDecorator {

    public WhipDecorator(Coffee coffee) {
        super(coffee);
    }

    @Override
    public double getCost() {
        return super.getCost() + 3.5;
    }

    @Override
    public String getDescription() {
        return super.getDescription() + ", Whip";
    }
}
