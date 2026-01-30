// list-containers.js
// 功能：列出当前所有容器（包括已停止的）

const Docker = require('dockerode');
const docker = new Docker();

async function listContainers() {
  try {
    // 获取所有容器（包括非运行中）
    const containers = await docker.listContainers({
      all: true // 包括已停止的容器
    });

    console.log('📊 当前容器列表：');
    containers.forEach((info) => {
      const state = info.State === 'running' ? '运行' : '停止';
      const names = info.Names.map(n => n.replace(/^//, '')).join(', '); // 去除开头的 /
      console.log(`- ${state}  ${names}`);
    });
  } catch (err) {
    console.error('❌ 列出容器失败:', err.message);
  }
}

listContainers();