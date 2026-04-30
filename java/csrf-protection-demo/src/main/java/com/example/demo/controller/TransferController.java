package com.example.demo.controller;

import com.example.demo.model.TransferRequest;
import com.example.demo.service.TransferService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/transfer")
public class TransferController {

    @Autowired
    private TransferService transferService;

    @PostMapping
    public ResponseEntity<Map<String, Object>> transfer(
            @RequestBody TransferRequest request,
            @AuthenticationPrincipal UserDetails userDetails) {
        Map<String, Object> result = transferService.processTransfer(
                userDetails.getUsername(),
                request.getToAccount(),
                request.getAmount()
        );
        return ResponseEntity.ok(result);
    }

    @GetMapping("/history")
    public ResponseEntity<Map<String, Object>> getHistory(
            @AuthenticationPrincipal UserDetails userDetails) {
        Map<String, Object> history = transferService.getTransferHistory(userDetails.getUsername());
        return ResponseEntity.ok(history);
    }
}
