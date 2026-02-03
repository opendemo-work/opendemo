package main

import (
	"fmt"
	"log"

	"github.com/dgraph-io/badger/v3"
)

// iterator.go 演示如何安全遍历BadgerDB中所有的键值对
func main() {
	// 使用相同选项打开数据库
	opt := badger.DefaultOptions("./badger-data")
	db, err := badger.Open(opt)
	if err != nil {
		log.Fatal("❌ 打开数据库失败: ", err)
	}
	defer func() {
		if err := db.Close(); err != nil {
			log.Printf("⚠️ 关闭数据库时出错: %v", err)
		}
	}()

	// 创建只读事务进行遍历
	err = db.View(func(txn *badger.Txn) error {
		// 创建默认迭代器
		it := txn.NewIterator(badger.DefaultIteratorOptions)
		defer it.Close() // 确保释放迭代器资源

		fmt.Println("\n🔍 当前数据库内容:")
		// Rewind 将迭代器移到第一个键
		for it.Rewind(); it.Valid(); it.Next() {
			item := it.Item()
			// Key() 返回的是只读引用，可直接使用
			k := item.Key()
			// Value() 必须在回调中调用以保证数据有效性
			var v []byte
			err := item.Value(func(val []byte) error {
				v = append([]byte{}, val...)
				return nil
			})
			if err != nil {
				return err
			}
			fmt.Printf("key: %s, value: %s\n", string(k), string(v))
		}
		return nil
	})
	if err != nil {
		log.Fatal("❌ 遍历失败: ", err)
	}
}