"""
Streamlit 启动包装器
在启动 Streamlit 之前设置正确的事件循环策略以兼容 Python 3.13+
"""
import sys
import os

# 必须在导入任何其他模块之前设置事件循环策略
if sys.platform == 'win32' and sys.version_info >= (3, 8):
    import asyncio
    # 设置 WindowsSelectorEventLoopPolicy 以支持子进程
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# 导入并运行 Streamlit
if __name__ == "__main__":
    import subprocess
    
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(current_dir, "app.py")
    
    # 使用 subprocess 启动 streamlit，确保事件循环策略已设置
    subprocess.run([sys.executable, "-m", "streamlit", "run", app_path])
