import numpy as np
import matplotlib.pyplot as plt

# 设置随机种子
np.random.seed(42)

# === 参数设置 ===
fs = 100  # 采样频率 (Hz)
T = 1.0 / fs  # 采样间隔
N = 200  # 采样点数
t = np.linspace(0, N * T, N)  # 时间轴

# === 生成包含两个频率的复合信号 ===
signal = (
    np.sin(2 * np.pi * 2 * t) +      # 2Hz 分量
    0.5 * np.sin(2 * np.pi * 7 * t)   # 7Hz 分量
)

# === 执行快速傅里叶变换 ===
fft_values = np.fft.fft(signal)

# === 计算对应频率值 ===
frequencies = np.fft.fftfreq(N, T)

# === 取正频率部分并归一化幅度 ===
half_n = N // 2
frequencies = frequencies[:half_n]
fft_magnitude = np.abs(fft_values[:half_n]) * (2 / N)

# === 可视化结果 ===
plt.figure(figsize=(12, 6))

# 时域信号
plt.subplot(2, 1, 1)
plt.plot(t, signal)
plt.title('时域信号: 2Hz 和 7Hz 的合成波')
plt.xlabel('时间 (s)')
plt.ylabel('幅度')
plt.grid(True)

# 频域频谱
plt.subplot(2, 1, 2)
plt.stem(frequencies, fft_magnitude, basefmt=" ", use_line_collection=True)
plt.title('频域表示: 显示出两个主频率峰值')
plt.xlabel('频率 (Hz)')
plt.ylabel('幅度')
plt.grid(True)

plt.tight_layout()
plt.show()