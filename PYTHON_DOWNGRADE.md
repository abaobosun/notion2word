# Python 3.12 降级指南

## 步骤 1: 下载 Python 3.12

1. 访问 Python 官方网站下载页面:
   **https://www.python.org/downloads/**

2. 找到 **Python 3.12** 最新版本（例如 3.12.7）

3. 根据您的系统选择：
   - **Windows 64位**: Windows installer (64-bit)
   - **Windows 32位**: Windows installer (32-bit)

4. 下载完成后运行安装程序

## 步骤 2: 安装 Python 3.12

### 重要选项设置:

1. ✅ **勾选** "Add Python 3.12 to PATH"（非常重要）
2. 选择 "Install Now" 或 "Customize installation"
3. 如果选择自定义:
   - ✅ pip
   - ✅ tcl/tk and IDLE
   - ✅ Python test suite
   - ✅ py launcher
   - ✅ for all users (optional)

### 卸载旧版本:

- **建议**: 安装 Python 3.12 后，卸载 Python 3.13
- 打开"设置" > "应用" > 搜索 "Python 3.13" > 卸载

## 步骤 3: 验证安装

打开新的命令提示符（必须是新的），运行：

```bash
python --version
```

应该显示：`Python 3.12.x`

## 步骤 4: 重新安装项目依赖

进入项目目录并重新安装依赖：

```bash
cd E:\goldensun\the-box\01Inbox\Downloads\notion2Word
pip install -r requirements.txt
playwright install chromium
```

## 步骤 5: 测试运行

双击 `启动程序.bat`，应该可以正常运行了。

---

## 快速下载链接

**Python 3.12.7 (Windows 64-bit)**:
https://www.python.org/ftp/python/3.12.7/python-3.12.7-amd64.exe

**Python 3.12.7 (Windows 32-bit)**:
https://www.python.org/ftp/python/3.12.7/python-3.12.7.exe

---

## 常见问题

### Q: 安装后还是显示 Python 3.13？
A: 关闭所有命令提示符和编辑器窗口，重新打开。如果还不行，重启电脑。

### Q: 能否同时保留两个版本？
A: 可以，但需要使用 `py -3.12` 而不是 `python` 来指定版本。

### Q: 卸载 Python 3.13 会影响其他程序吗？
A: 如果其他程序依赖 Python 3.13，可能会受影响。建议先安装 3.12，测试本项目可用后再决定是否卸载 3.13。
