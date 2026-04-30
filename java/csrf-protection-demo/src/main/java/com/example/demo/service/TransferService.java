package com.example.demo.service;

import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.*;

@Service
public class TransferService {

    private final Map<String, Double> accounts = new HashMap<>();
    private final List<Map<String, Object>> transferHistory = Collections.synchronizedList(new ArrayList<>());

    public TransferService() {
        accounts.put("alice", 10000.00);
        accounts.put("bob", 20000.00);
    }

    public Map<String, Object> processTransfer(String fromUser, String toAccount, double amount) {
        Map<String, Object> result = new LinkedHashMap<>();

        if (amount <= 0) {
            result.put("status", "FAILED");
            result.put("message", "转账金额必须大于零");
            return result;
        }

        Double balance = accounts.getOrDefault(fromUser, 0.0);
        if (balance < amount) {
            result.put("status", "FAILED");
            result.put("message", "余额不足");
            return result;
        }

        accounts.put(fromUser, balance - amount);
        accounts.merge(toAccount, amount, Double::sum);

        Map<String, Object> record = new LinkedHashMap<>();
        record.put("from", fromUser);
        record.put("to", toAccount);
        record.put("amount", amount);
        record.put("timestamp", LocalDateTime.now().toString());
        record.put("status", "SUCCESS");
        transferHistory.add(record);

        result.put("status", "SUCCESS");
        result.put("message", "转账成功");
        result.put("amount", amount);
        result.put("remainingBalance", accounts.get(fromUser));
        return result;
    }

    public Map<String, Object> getTransferHistory(String username) {
        Map<String, Object> result = new LinkedHashMap<>();
        List<Map<String, Object>> userHistory = new ArrayList<>();
        for (Map<String, Object> record : transferHistory) {
            if (username.equals(record.get("from")) || username.equals(record.get("to"))) {
                userHistory.add(record);
            }
        }
        result.put("username", username);
        result.put("balance", accounts.getOrDefault(username, 0.0));
        result.put("transfers", userHistory);
        return result;
    }
}
