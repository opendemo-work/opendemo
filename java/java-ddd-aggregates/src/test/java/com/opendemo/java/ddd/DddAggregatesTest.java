package com.opendemo.java.ddd;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import static org.junit.jupiter.api.Assertions.*;

class DddAggregatesTest {
    private OrderRepository repository;
    private OrderService service;

    @BeforeEach
    void setUp() {
        repository = new InMemoryOrderRepository();
        service = new OrderService(repository);
    }

    @Test
    void createOrderAndFindById() {
        OrderId id = new OrderId("ORD-001");
        CustomerId custId = new CustomerId("CUST-001");
        Order order = service.createOrder(id, custId);
        assertTrue(repository.findById(id).isPresent());
        assertEquals(OrderStatus.DRAFT, order.getStatus());
    }

    @Test
    void addProductToOrder() {
        OrderId id = new OrderId("ORD-002");
        service.createOrder(id, new CustomerId("CUST-001"));
        Order updated = service.addProductToOrder(id, new ProductId("PROD-001"), 2, new Money(50.0));
        assertEquals(1, updated.getOrderLines().size());
        assertEquals(new Money(100.0), updated.getTotal());
    }

    @Test
    void addMultipleProductsComputesTotal() {
        OrderId id = new OrderId("ORD-003");
        service.createOrder(id, new CustomerId("CUST-001"));
        service.addProductToOrder(id, new ProductId("PROD-001"), 2, new Money(30.0));
        service.addProductToOrder(id, new ProductId("PROD-002"), 1, new Money(100.0));
        Order order = repository.findById(id).orElseThrow();
        assertEquals(new Money(160.0), order.getTotal());
    }

    @Test
    void submitOrderChangesStatusAndPublishesEvent() {
        OrderId id = new OrderId("ORD-004");
        service.createOrder(id, new CustomerId("CUST-001"));
        service.addProductToOrder(id, new ProductId("PROD-001"), 1, new Money(10.0));
        Order submitted = service.submitOrder(id);
        assertEquals(OrderStatus.SUBMITTED, submitted.getStatus());
        assertFalse(submitted.getUncommittedEvents().isEmpty());
        assertTrue(submitted.getUncommittedEvents().get(0) instanceof OrderSubmittedEvent);
    }

    @Test
    void cannotSubmitEmptyOrder() {
        OrderId id = new OrderId("ORD-005");
        service.createOrder(id, new CustomerId("CUST-001"));
        assertThrows(IllegalStateException.class, () -> service.submitOrder(id));
    }

    @Test
    void cannotModifySubmittedOrder() {
        OrderId id = new OrderId("ORD-006");
        service.createOrder(id, new CustomerId("CUST-001"));
        service.addProductToOrder(id, new ProductId("PROD-001"), 1, new Money(10.0));
        service.submitOrder(id);
        assertThrows(IllegalStateException.class, () ->
                service.addProductToOrder(id, new ProductId("PROD-002"), 1, new Money(20.0)));
    }

    @Test
    void confirmOrder() {
        OrderId id = new OrderId("ORD-007");
        service.createOrder(id, new CustomerId("CUST-001"));
        service.addProductToOrder(id, new ProductId("PROD-001"), 1, new Money(10.0));
        service.submitOrder(id);
        Order confirmed = service.confirmOrder(id);
        assertEquals(OrderStatus.CONFIRMED, confirmed.getStatus());
    }

    @Test
    void cancelDraftOrder() {
        OrderId id = new OrderId("ORD-008");
        service.createOrder(id, new CustomerId("CUST-001"));
        Order cancelled = service.cancelOrder(id);
        assertEquals(OrderStatus.CANCELLED, cancelled.getStatus());
    }

    @Test
    void moneyOperations() {
        Money m1 = new Money(100.0);
        Money m2 = new Money(50.0);
        assertEquals(new Money(150.0), m1.add(m2));
        assertEquals(new Money(50.0), m1.subtract(m2));
        assertEquals(new Money(200.0), m1.multiply(2));
        assertTrue(m1.isGreaterThan(m2));
        assertTrue(m2.isLessThanOrEqual(m1));
    }

    @Test
    void addressEquality() {
        Address a1 = new Address("123 Main St", "Springfield", "62701");
        Address a2 = new Address("123 Main St", "Springfield", "62701");
        Address a3 = new Address("456 Oak Ave", "Shelbyville", "62565");
        assertEquals(a1, a2);
        assertNotEquals(a1, a3);
    }

    @Test
    void valueObjectEquality() {
        OrderId id1 = new OrderId("ORD-001");
        OrderId id2 = new OrderId("ORD-001");
        OrderId id3 = new OrderId("ORD-002");
        assertEquals(id1, id2);
        assertNotEquals(id1, id3);
    }

    @Test
    void findByCustomerId() {
        CustomerId cust1 = new CustomerId("CUST-001");
        CustomerId cust2 = new CustomerId("CUST-002");
        service.createOrder(new OrderId("ORD-A"), cust1);
        service.createOrder(new OrderId("ORD-B"), cust1);
        service.createOrder(new OrderId("ORD-C"), cust2);
        assertEquals(2, repository.findByCustomerId(cust1).size());
        assertEquals(1, repository.findByCustomerId(cust2).size());
    }

    @Test
    void orderItemChangeQuantity() {
        OrderItem item = new OrderItem(1, new ProductId("P1"), 3, new Money(25.0));
        assertEquals(new Money(75.0), item.getSubtotal());
        item.changeQuantity(5);
        assertEquals(5, item.getQuantity());
        assertEquals(new Money(125.0), item.getSubtotal());
    }
}
