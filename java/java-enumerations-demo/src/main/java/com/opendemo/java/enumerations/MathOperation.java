package com.opendemo.java.enumerations;

public enum MathOperation implements Operation {
    ADD("+") {
        @Override
        public double apply(double a, double b) {
            return a + b;
        }
    },
    SUBTRACT("-") {
        @Override
        public double apply(double a, double b) {
            return a - b;
        }
    },
    MULTIPLY("*") {
        @Override
        public double apply(double a, double b) {
            return a * b;
        }
    },
    DIVIDE("/") {
        @Override
        public double apply(double a, double b) {
            if (b == 0) {
                throw new ArithmeticException("除数不能为零");
            }
            return a / b;
        }
    };

    private final String symbol;

    MathOperation(String symbol) {
        this.symbol = symbol;
    }

    public String getSymbol() {
        return symbol;
    }

    public static MathOperation fromSymbol(String symbol) {
        for (MathOperation op : values()) {
            if (op.symbol.equals(symbol)) {
                return op;
            }
        }
        throw new IllegalArgumentException("未知运算符: " + symbol);
    }
}
