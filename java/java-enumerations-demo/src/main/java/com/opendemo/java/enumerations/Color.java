package com.opendemo.java.enumerations;

public enum Color {
    RED("红色", "#FF0000"),
    GREEN("绿色", "#00FF00"),
    BLUE("蓝色", "#0000FF"),
    YELLOW("黄色", "#FFFF00"),
    BLACK("黑色", "#000000"),
    WHITE("白色", "#FFFFFF");

    private final String name;
    private final String hexCode;

    Color(String name, String hexCode) {
        this.name = name;
        this.hexCode = hexCode;
    }

    public String getName() {
        return name;
    }

    public String getHexCode() {
        return hexCode;
    }

    public boolean isPrimary() {
        return this == RED || this == GREEN || this == BLUE;
    }

    public static Color fromName(String name) {
        for (Color color : values()) {
            if (color.name.equals(name)) {
                return color;
            }
        }
        throw new IllegalArgumentException("未知颜色名称: " + name);
    }

    public static Color fromHexCode(String hexCode) {
        for (Color color : values()) {
            if (color.hexCode.equalsIgnoreCase(hexCode)) {
                return color;
            }
        }
        throw new IllegalArgumentException("未知颜色代码: " + hexCode);
    }

    @Override
    public String toString() {
        return name + "(" + hexCode + ")";
    }
}
