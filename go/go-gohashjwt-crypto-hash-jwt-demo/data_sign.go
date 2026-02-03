package main

import (
	"crypto/hmac"
	"crypto/sha256"
	"encoding/hex"
	"fmt"
)

var secretKey = []byte("data_signing_key")

// signData 对数据进行HMAC-SHA256签名
func signData(data string) string {
	mac := hmac.New(sha256.New, secretKey)
	mac.Write([]byte(data))
	return hex.EncodeToString(mac.Sum(nil))
}

// verifyData 验证数据签名是否有效
func verifyData(data, signature string) bool {
	expected := signData(data)
	return hmac.Equal([]byte(signature), []byte(expected))
}

func main() {
	data := "important_payload_123"
	signature := signData(data)
	fmt.Printf("数据签名成功: %s\n", signature)

	isValid := verifyData(data, signature)
	fmt.Printf("数据验证通过: %t\n", isValid)
}