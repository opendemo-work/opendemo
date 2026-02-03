"""
文件: bit_flags.py
功能: 使用位运算管理应用程序的多项设置（位标志）
作者: Python导师
日期: 2023
"""

# 定义设置标志，每个设置占用一个二进制位
SOUND_ON = 1 << 0        # 0b0001
MUSIC_ON = 1 << 1        # 0b0010
AUTO_SAVE_ON = 1 << 2    # 0b0100
HIGH_CONTRAST_ON = 1 << 3 # 0b1000


def display_settings(flags):
    """
    显示当前所有设置的状态
    :param flags: 设置标志整数值
    """
    sound = "开" if flags & SOUND_ON else "关"
    music = "开" if flags & MUSIC_ON else "关"
    auto_save = "开" if flags & AUTO_SAVE_ON else "关"
    high_contrast = "开" if flags & HIGH_CONTRAST_ON else "关"
    
    print(f"当前设置: 音效{sound}, 音乐{music}, 自动保存{auto_save}, 高对比度{high_contrast}")


def toggle_music(flags):
    """
    切换音乐开关状态
    使用异或操作：相同为0，不同为1，实现翻转效果
    :param flags: 当前设置值
    :return: 新的设置值
    """
    return flags ^ MUSIC_ON


def is_enabled(flags, flag):
    """
    检查某个设置是否启用
    :param flags: 当前设置值
    :param flag: 要检查的标志
    :return: 布尔值
    """
    return (flags & flag) != 0


# 主程序演示
if __name__ == "__main__":
    # 初始化设置：音效开、音乐关、自动保存开、高对比度关
    settings = SOUND_ON | AUTO_SAVE_ON  # 0b0101
    
    print("初始设置: 音效开, 音乐关, 自动保存开, 高对比度关")
    
    # 切换音乐状态（从关→开）
    print("切换音乐状态...")
    settings = toggle_music(settings)
    display_settings(settings)
    
    # 启用高对比度模式
    print("启用高对比度模式...")
    settings |= HIGH_CONTRAST_ON  # 使用 |= 简化赋值
    display_settings(settings)
    
    # 检查自动保存是否启用
    print(f"是否启用了自动保存? {'是' if is_enabled(settings, AUTO_SAVE_ON) else '否'}")