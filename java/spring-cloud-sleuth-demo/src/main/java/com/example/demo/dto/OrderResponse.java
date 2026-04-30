package com.example.demo.dto;

public class OrderResponse {

    private String orderId;
    private String productId;
    private String status;
    private String paymentId;

    public OrderResponse(String orderId, String productId, String status, String paymentId) {
        this.orderId = orderId;
        this.productId = productId;
        this.status = status;
        this.paymentId = paymentId;
    }

    public String getOrderId() {
        return orderId;
    }

    public void setOrderId(String orderId) {
        this.orderId = orderId;
    }

    public String getProductId() {
        return productId;
    }

    public void setProductId(String productId) {
        this.productId = productId;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getPaymentId() {
        return paymentId;
    }

    public void setPaymentId(String paymentId) {
        this.paymentId = paymentId;
    }
}
