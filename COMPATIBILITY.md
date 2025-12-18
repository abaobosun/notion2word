# Python 版本兼容性说明

## 问题
如果您使用 Python 3.13 在 Windows 上运行此程序，可能会遇到以下错误：

```
NotImplementedError
  File "asyncio\base_events.py", line 534, in _make_subprocess_transport
    raise NotImplementedError
```

## 原因
这是 Python 3.13 在 Windows 上与 Playwright 库的已知兼容性问题。Python 3.13 更改了默认的 asyncio 事件循环策略，而 Playwright 的同步 API 依赖于子进程功能，在新的事件循环下无法正常工作。

## 解决方案

### 方案一：使用推荐的 Python 版本 (推荐)
降级到 **Python 3.11** 或 **3.12**，这是最简单和最稳定的解决方案。

### 方案二：安装兼容性补丁 (高级)
如果必须使用 Python 3.13，可以：

1. 安装 `nest-asyncio` 包:
   ```bash
   pip install nest-asyncio
   ```

2. 在运行前设置环境变量:
   ```bash
   set PLAYWRIGHT_BROWSERS_PATH=0
   ```

3. 或者使用命令行模式而不是 Web 界面:
   ```bash
   python main.py <URL> -o output.docx
   ```

### 方案三：等待官方修复
Playwright 团队正在解决此问题。您可以关注官方 GitHub issue 获取最新进展。

## 推荐配置
- **操作系统**: Windows 10/11, macOS, Linux
- **Python 版本**: 3.11 或 3.12
- **内存**: 至少 2GB RAM
