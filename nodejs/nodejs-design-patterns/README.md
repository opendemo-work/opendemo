# Node.js Design Patterns

Node.js设计模式实践。

## 核心模式

### 1. 模块模式
```javascript
// myModule.js
const privateVariable = 'private';

function privateFunction() {
    return privateVariable;
}

module.exports = {
    publicMethod: function() {
        return privateFunction();
    }
};
```

### 2. 观察者模式 (EventEmitter)
```javascript
const EventEmitter = require('events');

class MyEmitter extends EventEmitter {}

const myEmitter = new MyEmitter();

myEmitter.on('event', (data) => {
    console.log('Event received:', data);
});

myEmitter.emit('event', { message: 'Hello' });
```

### 3. 工厂模式
```javascript
class User {
    constructor(name) {
        this.name = name;
    }
}

class Admin extends User {
    constructor(name) {
        super(name);
        this.role = 'admin';
    }
}

class UserFactory {
    static create(type, name) {
        switch(type) {
            case 'user': return new User(name);
            case 'admin': return new Admin(name);
            default: throw new Error('Unknown type');
        }
    }
}
```

### 4. 中间件模式
```javascript
function middleware1(req, res, next) {
    console.log('Middleware 1');
    next();
}

function middleware2(req, res, next) {
    console.log('Middleware 2');
    next();
}

function handler(req, res) {
    console.log('Handler');
}

// 执行链
const stack = [middleware1, middleware2, handler];

function run(req, res) {
    let index = 0;
    function next() {
        if (index < stack.length) {
            stack[index++](req, res, next);
        }
    }
    next();
}
```

## 异步模式

```javascript
// Callbacks
def readFileCallback() {
    fs.readFile('file.txt', (err, data) => {
        if (err) throw err;
        console.log(data);
    });
}

// Promises
def readFilePromise() {
    return fs.promises.readFile('file.txt')
        .then(data => console.log(data))
        .catch(err => console.error(err));
}

// Async/Await
async function readFileAsync() {
    try {
        const data = await fs.promises.readFile('file.txt');
        console.log(data);
    } catch (err) {
        console.error(err);
    }
}
```

## 学习要点

1. CommonJS模块
2. EventEmitter模式
3. 回调与Promise
4. 中间件链
5. 流处理模式
