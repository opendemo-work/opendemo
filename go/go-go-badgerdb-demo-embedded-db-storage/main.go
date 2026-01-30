package main

import (
	"fmt"
	"log"

	"github.com/dgraph-io/badger/v3"
)

// main 函数演示基本的BadgerDB操作：打开数据库、增删改查、事务处理
func main() {
	// 配置并打开Badger数据库，数据存储在本地目录
	opt := badger.DefaultOptions("./badger-data")
	db, err := badger.Open(opt)
	if err != nil {
		log.Fatal("❌ 打开数据库失败: ", err)
	}
	// 确保程序结束时关闭数据库，释放文件锁和内存
	defer func() {
		if err := db.Close(); err != nil {
			log.Printf("⚠️ 关闭数据库时出错: %v", err)
		}
	}()

	// 示例1: 写入新键值对 (Put)
	err = db.Update(func(txn *badger.Txn) error {
		err := txn.Set([]byte("name"), []byte("Gopher"))
		if err != nil {
			return err
		}
		fmt.Println("✅ 成功写入: name -> Gopher")
		return nil
	})
	if err != nil {
		log.Fatal("❌ 写入失败: ", err)
	}

	// 示例2: 读取键值 (Get)
	err = db.View(func(txn *badger.Txn) error {
		item, err := txn.Get([]byte("name"))
		if err != nil {
			return err
		}
		// 获取实际值（需复制）
		var val []byte
		err = item.Value(func(valCopy []byte) error {
			val = append([]byte{}, valCopy...)
			return nil
		})
		if err != nil {
			return err
		}
		fmt.Printf("✅ 成功读取: name = %s\n", string(val))
		return nil
	})
	if err != nil {
		log.Fatal("❌ 读取失败: ", err)
	}

	// 示例3: 更新计数器（模拟访问次数）
	err = db.Update(func(txn *badger.Txn) error {
		// 先尝试获取现有值
		item, err := txn.Get([]byte("visits"))
		var count int
		if err == nil {
			err = item.Value(func(val []byte) error {
			fmt.Sscanf(string(val), "%d", &count)
			return nil
		})
		}
		count++
		// 更新或创建键
		if err = txn.Set([]byte("visits"), []byte(fmt.Sprintf("%d", count))); err != nil {
			return err
		}
		fmt.Printf("✅ 成功更新: visits -> %d\n", count)
		return nil
	})
	if err != nil {
		log.Fatal("❌ 更新失败: ", err)
	}

	// 示例4: 删除某个键
	er = db.Update(func(txn *badger.Txn) error {
		err := txn.Set([]byte("temp_data"), []byte("temporary"))
		if err != nil {
			return err
		}
		return txn.Delete([]byte("temp_data"))
	})
	if err != nil {
		log.Fatal("❌ 删除失败: ", err)
	}
	fmt.Println("✅ 成功删除: temp_data")
}