package com.example.demo.dto;

import java.util.Map;

public class ApiResponse {

    private int code;
    private String message;
    private Object data;
    private Map<String, String> errors;

    public ApiResponse(int code, String message, Object data, Map<String, String> errors) {
        this.code = code;
        this.message = message;
        this.data = data;
        this.errors = errors;
    }

    public static ApiResponse success(String message, Object data) {
        return new ApiResponse(200, message, data, null);
    }

    public static ApiResponse fail(String message, Map<String, String> errors) {
        return new ApiResponse(400, message, null, errors);
    }

    public int getCode() {
        return code;
    }

    public void setCode(int code) {
        this.code = code;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public Object getData() {
        return data;
    }

    public void setData(Object data) {
        this.data = data;
    }

    public Map<String, String> getErrors() {
        return errors;
    }

    public void setErrors(Map<String, String> errors) {
        this.errors = errors;
    }
}
