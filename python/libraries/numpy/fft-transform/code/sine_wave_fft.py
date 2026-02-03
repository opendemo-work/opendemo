import numpy as np
import matplotlib.pyplot as plt

# 设置随机种子以确保可重复性
np.random.seed(42)

# === 参数设置 ===
fs = 100  # 采样频率 (Hz)
T = 1.0 / fs  # 采样周期
N = 100  # 采样点数
t = np.linspace(0, N * T, N)  # 时间向量

# === 生成单一频率的正弦波信号 ===
frequency = 5  # 正弦波频率 (Hz)
signal = np.sin(2 * np.pi * frequency * t)

# === 执行快速傅里叶变换 (FFT) ===
fft_values = np.fft.fft(signal)

# === 生成对应的频率数组 ===
frequencies = np.fft.fftfreq(N, T)

# === 只取前半部分（正频率部分）===
# 因为实数信号的FFT是对称的，负频率部分是冗余的
half_n = N // 2
frequencies = frequencies[:half_n]
fft_magnitude = np.abs(fft_values[:half_n]) * (2 / N)  # 幅度归一化

# === 绘制时域和频域图形 ===
plt.figure(figsize=(12, 6))

# 绘制原始信号（时域）
plt.subplot(2, 1, 1)
plt.plot(t, signal)
plt.title('时域信号: 5Hz 正弦波')
plt.xlabel('时间 (s)')
plt.ylabel('幅度')
plt.grid(True)

# 绘制频谱（频域）
plt.subplot(2, 1, 2)
plt.stem(frequencies, fft_magnitude, basefmt=" ")
plt.title('频域表示: FFT 结果')
plt.xlabel('频率 (Hz)')
plt.ylabel('幅度')
plt.grid(True)

plt.tight_layout()
plt.show()