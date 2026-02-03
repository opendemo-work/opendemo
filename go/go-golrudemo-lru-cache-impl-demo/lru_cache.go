package main

// entry 表示缓存中的键值对，同时作为双向链表的节点
// 包含前后指针，用于维护访问顺序
// 最新使用的放在头部，最久未使用的在尾部
type entry struct {
	key   string // 键
	value int    // 值
	prev  *entry // 指向前一个节点的指针
	next  *entry // 指向后一个节点的指针
}

// LRUCache 是LRU缓存的核心结构
// 使用哈希表+双向链表实现O(1)时间复杂度的Get和Put操作
// cache: 哈希表，用于O(1)查找键是否存在
// head: 虚拟头节点，简化链表操作
// tail: 虚拟尾节点，简化链表操作
// capacity: 缓存最大容量
// size: 当前缓存中的元素数量
type LRUCache struct {
	cache    map[string]*entry
	head     *entry
	tail     *entry
	capacity int
	size     int
}

// Constructor 创建一个新的LRU缓存实例
// 初始化双向链表的虚拟头尾节点，并建立连接
// 使用map初始化哈希表存储空间
func Constructor(capacity int) LRUCache {
	lru := LRUCache{
		cache:    make(map[string]*entry),
		capacity: capacity,
		size:     0,
	}
	// 创建虚拟头尾节点，简化边界条件处理
	lru.head = &entry{}
	lru.tail = &entry{}
	// 建立头尾连接
	lru.head.next = lru.tail
	lru.tail.prev = lru.head
	return lru
}

// Get 从缓存中获取指定键的值
// 如果存在，将其移动到链表头部（标记为最新使用），并返回值和true
// 如果不存在，返回0和false
func (c *LRUCache) Get(key string) (int, bool) {
	if node, exists := c.cache[key]; exists {
		// 命中缓存：先从原位置删除，再移到头部
		c.remove(node)
		c.moveToHead(node)
		return node.value, true
	}
	// 未命中缓存
	return 0, false
}

// Put 向缓存中插入或更新键值对
// 如果键已存在，则更新其值并移到头部
// 如果键不存在：
//   - 若缓存已满，先删除尾部最久未使用元素
//   - 创建新节点并插入头部
func (c *LRUCache) Put(key string, value int) {
	if node, exists := c.cache[key]; exists {
		// 键已存在：更新值并移到头部
		node.value = value
		c.remove(node)
		c.moveToHead(node)
	} else {
		// 键不存在：检查是否需要淘汰
		if c.size >= c.capacity {
			// 删除尾部最久未使用节点
			removed := c.removeTail()
			delete(c.cache, removed.key)
			c.size--
		}
		// 创建新节点并加入缓存
		newNode := &entry{key: key, value: value}
		c.cache[key] = newNode
		c.moveToHead(newNode)
		c.size++
	}
}

// remove 从双向链表中删除指定节点
// 仅修改链表指针，不涉及哈希表操作
func (c *LRUCache) remove(node *entry) {
	node.prev.next = node.next
	node.next.prev = node.prev
}

// moveToHead 将指定节点移动到链表头部
// 先删除原位置，再插入头部
func (c *LRUCache) moveToHead(node *entry) {
	node.prev = c.head
	node.next = c.head.next
	c.head.next.prev = node
	c.head.next = node
}

// removeTail 删除并返回尾部节点（最久未使用）
// 用于缓存满时的淘汰操作
func (c *LRUCache) removeTail() *entry {
	last := c.tail.prev
	c.remove(last)
	return last
}