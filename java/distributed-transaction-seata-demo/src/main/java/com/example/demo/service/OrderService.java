package com.example.demo.service;

import io.seata.spring.annotation.GlobalTransactional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
 * 订单服务
 * 
 * 使用@GlobalTransactional开启Seata全局事务
 */
@Service
public class OrderService {
    
    @Autowired
    private StorageFeignClient storageFeignClient;
    
    @Autowired
    private AccountFeignClient accountFeignClient;
    
    @Autowired
    private OrderRepository orderRepository;
    
    /**
     * 创建订单 - 分布式事务
     * 
     * @GlobalTransactional: 标记全局事务入口
     * name: 事务名称
     * rollbackFor: 触发回滚的异常类型
     */
    @GlobalTransactional(name = "create-order", rollbackFor = Exception.class)
    public Order createOrder(Long userId, Long productId, Integer count) {
        // 1. 计算金额
        BigDecimal price = new BigDecimal("100.00");
        BigDecimal totalAmount = price.multiply(new BigDecimal(count));
        
        // 2. 创建订单
        Order order = new Order();
        order.setUserId(userId);
        order.setProductId(productId);
        order.setCount(count);
        order.setMoney(totalAmount);
        order.setStatus(0); // 0: 创建中
        
        orderRepository.save(order);
        System.out.println("[订单服务] 订单创建成功，订单ID: " + order.getId());
        
        // 3. 扣减库存 - 调用库存服务
        storageFeignClient.deduct(productId, count);
        System.out.println("[订单服务] 库存扣减成功");
        
        // 4. 扣减账户余额 - 调用账户服务
        accountFeignClient.debit(userId, totalAmount);
        System.out.println("[订单服务] 账户扣减成功");
        
        // 5. 更新订单状态
        order.setStatus(1); // 1: 已完成
        orderRepository.save(order);
        System.out.println("[订单服务] 订单完成");
        
        return order;
    }
}

/**
 * 订单实体
 */
@Entity
@Table(name = "t_order")
class Order {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private Long userId;
    private Long productId;
    private Integer count;
    private BigDecimal money;
    private Integer status;
    
    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public Long getUserId() { return userId; }
    public void setUserId(Long userId) { this.userId = userId; }
    public Long getProductId() { return productId; }
    public void setProductId(Long productId) { this.productId = productId; }
    public Integer getCount() { return count; }
    public void setCount(Integer count) { this.count = count; }
    public BigDecimal getMoney() { return money; }
    public void setMoney(BigDecimal money) { this.money = money; }
    public Integer getStatus() { return status; }
    public void setStatus(Integer status) { this.status = status; }
}

/**
 * Feign客户端 - 库存服务
 */
@FeignClient(name = "storage-service")
interface StorageFeignClient {
    @PostMapping("/storage/deduct")
    void deduct(@RequestParam("productId") Long productId, 
                @RequestParam("count") Integer count);
}

/**
 * Feign客户端 - 账户服务
 */
@FeignClient(name = "account-service")
interface AccountFeignClient {
    @PostMapping("/account/debit")
    void debit(@RequestParam("userId") Long userId, 
               @RequestParam("amount") BigDecimal amount);
}

/**
 * 订单数据访问
 */
interface OrderRepository extends JpaRepository<Order, Long> {}
