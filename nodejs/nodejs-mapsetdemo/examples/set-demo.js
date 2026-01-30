// set-demo.js - 演示Set数据结构的使用

// 创建Set实例并传入一个数组
// Set会自动去除重复元素，只保留唯一值
const numbers = [1, 2, 2, 3, 4, 4, 5];
const uniqueNumbers = new Set(numbers);

// 将Set转换为数组以便查看
const deduplicated = Array.from(uniqueNumbers);
// 或使用扩展运算符: [...uniqueNumbers]
console.log('原始数组:', numbers);
console.log('去重后:', deduplicated);

// Set还支持动态添加
const tagSet = new Set();
tagSet.add('javascript');
tagSet.add('nodejs');
tagSet.add('javascript'); // 重复添加无效
console.log('标签数量:', tagSet.size); // 输出: 2

// 演示集合运算：交集、并集、差集
const setA = new Set([1, 2, 3]);
const setB = new Set([2, 3, 4, 5, 6]);

// 交集：存在于A和B中的元素
const intersection = [...setA].filter(x => setB.has(x));
console.log('交集:', intersection);

// 并集：存在于A或B中的所有唯一元素
const union = new Set([...setA, ...setB]);
console.log('并集:', [...union]);

// 差集：存在于A但不在B中的元素
const difference = [...setA].filter(x => !setB.has(x));
console.log('差集:', difference);