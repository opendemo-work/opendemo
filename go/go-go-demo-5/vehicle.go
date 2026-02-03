package main

// Vehicle 定义交通工具的行为接口
// 只要实现 Drive 方法即可被视为 Vehicle
type Vehicle interface {
	Drive()
}

// Car 表示汽车
type Car struct {
	Speed int // 当前速度，单位 km/h
}

// Drive 实现 Vehicle 接口
// 输出汽车行驶状态
func (c *Car) Drive() {
	fmt.Printf("汽车正在行驶，速度：%d km/h\n", c.Speed)
}

// Bicycle 表示自行车
type Bicycle struct {
	Speed int // 当前速度，单位 km/h
}

// Drive 实现 Vehicle 接口
// 输出自行车骑行状态
func (b *Bicycle) Drive() {
	fmt.Printf("自行车正在行驶，速度：%d km/h\n", b.Speed)
}