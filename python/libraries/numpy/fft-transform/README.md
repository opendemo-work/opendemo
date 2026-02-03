# 傅里叶变换FFT实战演示

## 简介
本项目通过两个具体的Python示例，帮助初学者理解快速傅里叶变换（FFT）的基本原理和实际应用。我们将使用`numpy`进行FFT计算，`matplotlib`进行信号可视化，展示时域信号如何转换为频域表示。

## 学习目标
- 理解傅里叶变换的基本概念及其在信号处理中的作用
- 掌握使用`numpy.fft`模块进行FFT计算的方法
- 能够将时域信号转换为频域并可视化结果
- 学会识别合成信号中的主要频率成分

## 环境要求
- Python 3.8 或更高版本
- 操作系统：Windows / Linux / macOS（均支持）

## 安装依赖步骤

1. 确保已安装Python和pip：
```bash
python --version
pip --version
```

2. 创建虚拟环境（推荐）：
```bash
python -m venv fft_env
```

3. 激活虚拟环境：
- Windows:
```bash
fft_env\Scripts\activate
```
- Linux/macOS:
```bash
source fft_env/bin/activate
```

4. 安装所需依赖：
```bash
pip install -r requirements.txt
```

## 文件说明
- `code/sine_wave_fft.py`: 分析单频正弦波的FFT
- `code/combined_signal_fft.py`: 分析多频率组合信号的FFT
- `requirements.txt`: 项目依赖声明文件

## 逐步实操指南

### 步骤1：运行正弦波FFT示例
```bash
python code/sine_wave_fft.py
```
**预期输出**：弹出一个包含时域波形和频域频谱图的窗口，显示单一峰值。

### 步骤2：运行复合信号FFT示例
```bash
python code/combined_signal_fft.py
```
**预期输出**：弹出图形窗口，显示由两个频率组成的信号及其对应的双峰频谱图。

## 代码解析

### sine_wave_fft.py 关键点
- 使用`np.sin`生成频率为5Hz的正弦波
- `np.fft.fft()`执行快速傅里叶变换
- `np.fft.fftfreq()`生成对应频率数组
- 只绘制前半部分频谱（因对称性），便于观察

### combined_signal_fft.py 关键点
- 合成信号包含2Hz和7Hz两个频率分量
- 频谱图中会在对应频率位置出现明显峰值
- 展示了FFT如何分离混合信号中的不同频率

## 预期输出示例
```
--- sine_wave_fft.py 输出 ---
打开图形窗口：
- 上图：5Hz正弦波（时域）
- 下图：在5Hz处有一个显著峰值（频域）

--- combined_signal_fft.py 输出 ---
打开图形窗口：
- 上图：2Hz + 7Hz合成波形
- 下图：在2Hz和7Hz位置有两个清晰峰值
```

## 常见问题解答

**Q: 为什么频谱只画了一半？**
A: 因为实数信号的FFT结果是对称的，后半部分是前半部分的镜像，因此只需观察前半部分即可。

**Q: 如何识别频谱中的频率值？**
A: 使用`np.fft.fftfreq(N, T)`可以获得每个FFT点对应的频率值，横轴即为此数组的前半段。

**Q: 图形没有弹出怎么办？**
A: 尝试在代码末尾添加`plt.show()`，或检查是否安装了正确的后端（如Tkinter）。

**Q: 可以处理真实音频数据吗？**
A: 可以！后续可扩展读取.wav文件，进行音频频谱分析。

## 扩展学习建议
- 尝试添加噪声并观察频谱变化
- 使用`scipy.fft`替代`numpy.fft`以获得更高性能
- 实现逆FFT（IFFT）还原原始信号
- 对真实音频文件（.wav）进行频谱分析
- 学习短时傅里叶变换（STFT）用于时频分析