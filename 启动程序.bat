@echo off
chcp 65001 > nul
echo ========================================================
echo        📝 Notion 转 Word 启动器 (Web UI)
echo ========================================================
echo.
echo 正在启动网页界面，请稍候...
echo 浏览器将自动打开，如未打开请手动访问: http://localhost:5000
echo.

py web_app.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ 启动失败！
    echo.
    echo 可能的原因:
    echo 1. 未安装依赖: py -m pip install flask
    echo 2. 端口 5000 被占用
    echo.
    pause
)
