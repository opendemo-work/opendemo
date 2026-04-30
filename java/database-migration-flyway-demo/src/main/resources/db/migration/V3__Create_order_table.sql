CREATE TABLE customer_order (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    customer_id BIGINT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL DEFAULT 0,
    status VARCHAR(20) DEFAULT 'PENDING',
    CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES customer(id)
);

CREATE INDEX idx_order_customer_id ON customer_order(customer_id);
CREATE INDEX idx_order_status ON customer_order(status);
