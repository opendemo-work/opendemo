package main

// Vehicle 表示交通工具的基本信息
type Vehicle struct {
	Brand string // 品牌
	Model string // 型号
}

// Car 表示汽车，组合了Person和Vehicle
// 使用匿名字段实现字段提升，可以直接访问Brand、Model等字段
// 这是Go中实现“继承”特性的推荐方式——组合优于继承
type Car struct {
	Person  // 匿名嵌入Person，可直接访问Name、Age
	Vehicle // 匿名嵌入Vehicle，可直接访问Brand、Model
	// 注意：如果两个嵌入结构体有同名字段，需显式调用 p.Person.Name
}