package com.opendemo.java.ddd;

public class OrderItem extends Entity<Integer> {
    private final ProductId productId;
    private int quantity;
    private Money price;

    public OrderItem(int lineNumber, ProductId productId, int quantity, Money price) {
        super(lineNumber);
        this.productId = productId;
        this.quantity = quantity;
        this.price = price;
    }

    public ProductId getProductId() {
        return productId;
    }

    public int getQuantity() {
        return quantity;
    }

    public Money getPrice() {
        return price;
    }

    public Money getSubtotal() {
        return price.multiply(quantity);
    }

    public void changeQuantity(int newQuantity) {
        if (newQuantity <= 0) {
            throw new IllegalArgumentException("Quantity must be positive");
        }
        this.quantity = newQuantity;
    }

    public void changePrice(Money newPrice) {
        this.price = newPrice;
    }
}
