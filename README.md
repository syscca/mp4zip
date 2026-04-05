# MP4 极限压缩工具 (Windows 11)

这是一个专为 Windows 11 设计的 MP4 视频极限压缩工具，基于 Python 和 FFmpeg 开发。它支持 H.264 和 H.265 (HEVC) 编码，并集成了 Intel Quick Sync Video (QSV) 硬件加速，能够在保持清晰画质的同时实现极高的压缩率。

## 功能特点

- **三种压缩模式**：
  - **标准 (H.264)**：高兼容性，速度快。
  - **强力 (H.265)**：推荐模式，画质与体积的最佳平衡。
  - **极限 (H.265 Slow)**：追求极致的小体积，适合深度存档。
- **硬件加速**：支持 Intel CPU 核显加速 (QSV)，显著降低 CPU 占用并提升速度。
- **中文界面**：简洁直观的 Tkinter 图形化操作界面。
- **进度实时显示**：压缩进度条、日志记录以及压缩前后体积对比。

## 安装说明

### 1. 前置要求

在开始之前，请确保你的系统已安装以下软件：

- **Python 3.x**：[从官网下载安装](https://www.python.org/downloads/)（安装时请勾选 "Add Python to PATH"）。
- **FFmpeg**：确保 `ffmpeg` 和 `ffprobe` 命令已添加到系统环境变量 PATH 中。

### 2. 下载与运行

你可以通过 Git 克隆仓库或直接下载源码：

```bash
# 克隆仓库
git clone https://github.com/syscca/mp4zip.git

# 进入目录
cd mp4zip

# 运行程序
python mp4zip.py
```

### 3. 使用步骤

1. 点击 **“浏览...”** 按钮选择需要压缩的 MP4 文件。
2. 根据需求选择 **“压缩强度”**。
3. 如果你的电脑使用 Intel 处理器，建议保持 **“开启英特尔核显加速 (QSV)”** 勾选状态。
4. 点击 **“开始压缩”**，等待完成后查看压缩结果。

## 开发者

- GitHub: [@syscca](https://github.com/syscca)

## 许可证

本项目采用 MIT 许可证。

