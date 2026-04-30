package com.opendemo.java.patterns.strategy;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;

import static org.junit.jupiter.api.Assertions.*;

import java.util.Arrays;

@DisplayName("策略模式测试")
class StrategyPatternTest {

    private PaymentContext paymentContext;
    private Sorter sorter;

    @BeforeEach
    void setUp() {
        paymentContext = new PaymentContext();
        sorter = new Sorter();
    }

    @Test
    @DisplayName("信用卡支付")
    void testCreditCardPayment() {
        paymentContext.setPaymentStrategy(new CreditCardPayment("1234567890123456", "Test", "12/28"));
        assertTrue(paymentContext.executePayment(100.0));
        assertEquals("Credit Card", paymentContext.getPaymentStrategy().getName());
    }

    @Test
    @DisplayName("支付宝支付")
    void testAlipayPayment() {
        paymentContext.setPaymentStrategy(new AlipayPayment("test@alipay.com"));
        assertTrue(paymentContext.executePayment(50.0));
        assertEquals("Alipay", paymentContext.getPaymentStrategy().getName());
    }

    @Test
    @DisplayName("微信支付")
    void testWeChatPayment() {
        paymentContext.setPaymentStrategy(new WeChatPayment("wx_test_id"));
        assertTrue(paymentContext.executePayment(30.0));
        assertEquals("WeChat Pay", paymentContext.getPaymentStrategy().getName());
    }

    @Test
    @DisplayName("未设置策略时支付失败")
    void testNoPaymentStrategy() {
        assertFalse(paymentContext.executePayment(100.0));
    }

    @Test
    @DisplayName("动态切换支付策略")
    void testSwitchPaymentStrategy() {
        paymentContext.setPaymentStrategy(new CreditCardPayment("1234", "Test", "12/28"));
        assertEquals("Credit Card", paymentContext.getPaymentStrategy().getName());

        paymentContext.setPaymentStrategy(new AlipayPayment("test@alipay.com"));
        assertEquals("Alipay", paymentContext.getPaymentStrategy().getName());
    }

    @Test
    @DisplayName("冒泡排序")
    void testBubbleSort() {
        int[] data = {64, 34, 25, 12, 22, 11, 90};
        int[] expected = {11, 12, 22, 25, 34, 64, 90};
        sorter.setSortingStrategy(new BubbleSort());
        sorter.sort(data);
        assertArrayEquals(expected, data);
    }

    @Test
    @DisplayName("快速排序")
    void testQuickSort() {
        int[] data = {64, 34, 25, 12, 22, 11, 90};
        int[] expected = {11, 12, 22, 25, 34, 64, 90};
        sorter.setSortingStrategy(new QuickSort());
        sorter.sort(data);
        assertArrayEquals(expected, data);
    }

    @Test
    @DisplayName("归并排序")
    void testMergeSort() {
        int[] data = {64, 34, 25, 12, 22, 11, 90};
        int[] expected = {11, 12, 22, 25, 34, 64, 90};
        sorter.setSortingStrategy(new MergeSort());
        sorter.sort(data);
        assertArrayEquals(expected, data);
    }

    @Test
    @DisplayName("空数组排序")
    void testSortEmptyArray() {
        int[] data = {};
        sorter.setSortingStrategy(new QuickSort());
        sorter.sort(data);
        assertArrayEquals(new int[]{}, data);
    }

    @Test
    @DisplayName("单元素数组排序")
    void testSortSingleElement() {
        int[] data = {42};
        sorter.setSortingStrategy(new BubbleSort());
        sorter.sort(data);
        assertArrayEquals(new int[]{42}, data);
    }

    @Test
    @DisplayName("已排序数组排序")
    void testSortAlreadySorted() {
        int[] data = {1, 2, 3, 4, 5};
        int[] expected = {1, 2, 3, 4, 5};
        sorter.setSortingStrategy(new MergeSort());
        sorter.sort(data);
        assertArrayEquals(expected, data);
    }

    @Test
    @DisplayName("所有排序算法结果一致")
    void testAllSortAlgorithmsProduceSameResult() {
        int[] original = {64, 34, 25, 12, 22, 11, 90, 1, 100, 55};
        int[] expected = original.clone();
        Arrays.sort(expected);

        int[] data1 = original.clone();
        sorter.setSortingStrategy(new BubbleSort());
        sorter.sort(data1);
        assertArrayEquals(expected, data1);

        int[] data2 = original.clone();
        sorter.setSortingStrategy(new QuickSort());
        sorter.sort(data2);
        assertArrayEquals(expected, data2);

        int[] data3 = original.clone();
        sorter.setSortingStrategy(new MergeSort());
        sorter.sort(data3);
        assertArrayEquals(expected, data3);
    }
}
