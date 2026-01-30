// container-manager.js
// 功能：创建、启动、获取日志、停止并删除一个容器

// 导入 Docker SDK
const Docker = require('dockerode');

// 创建默认连接（自动检测 socket 或 TCP）
const docker = new Docker();

async function main() {
  let container;

  try {
    // 步骤1：创建容器
    // 使用 alpine 镜像执行一条 echo 命令
    container = await docker.createContainer({
      Image: 'alpine',
      Cmd: ['echo', 'Hello from Alpine!'],
      name: 'my-test-container'
    });
    console.log(`✅ 容器已创建，ID: ${container.id.substring(0, 12)}`);

    // 步骤2：启动容器
    await container.start();
    console.log('✅ 容器已启动');

    // 步骤3：获取并打印日志
    console.log('📜 日志流开始...');
    const logStream = await container.logs({
      stdout: true,
      stderr: true,
      follow: true // 流式输出
    });

    // 将日志流转换为文本并输出
    logStream.on('data', (chunk) => {
      process.stdout.write(chunk.toString());
    });

    // 等待容器结束
    await container.wait();

    // 步骤4：停止容器（尽管已自动退出）
    await container.stop().catch(() => {}); // 忽略已停止的错误
    console.log('\n✅ 容器已停止');

    // 步骤5：删除容器
    await container.remove();
    console.log('🗑️ 容器已删除');

  } catch (err) {
    console.error('❌ 操作失败:', err.message);
    if (container) {
      // 清理：尝试删除容器以防残留
      try {
        await container.remove({ force: true });
        console.log('🧹 已强制清理残留容器');
      } catch (cleanupErr) {
        console.warn('⚠️ 清理失败:', cleanupErr.message);
      }
    }
  }
}

// 执行主函数
main();