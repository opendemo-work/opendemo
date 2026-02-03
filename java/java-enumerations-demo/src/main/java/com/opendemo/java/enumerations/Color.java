package com.opendemo.java.enumerations;

public enum Color {
    RED("红色", "#FF0000"),
    GREEN("绿色", "#00FF00"),
    BLUE("蓝色", "#0000FF");
    
    private String name;
    private String hexCode;
    
    Color(String name, String hexCode) {
        this.name = name;
        this.hexCode = hexCode;
    }
    
    public String getName() { return name; }
    public String getHexCode() { return hexCode; }
}