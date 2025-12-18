"""
Flask Web 界面 - Notion 转 Word 转换器
使用 Flask 替代 Streamlit 以避免事件循环冲突
"""
import sys
import os
import io

# 修复 Windows 事件循环策略
if sys.platform == 'win32':
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from flask import Flask, render_template_string, request, send_file, jsonify
from scraper import NotionScraper
from converter import NotionToWordConverter

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📝 Notion 转 Word 转换器</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
            max-width: 600px;
            width: 100%;
        }
        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 28px;
        }
        .subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 14px;
        }
        .input-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: 500;
        }
        input[type="text"], input[type="number"] {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            transition: border-color 0.3s;
        }
        input[type="text"]:focus, input[type="number"]:focus {
            outline: none;
            border-color: #667eea;
        }
        .checkbox-group {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }
        .checkbox-group input {
            margin-right: 8px;
        }
        button {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
        }
        button:active {
            transform: translateY(0);
        }
        button:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }
        .status {
            margin-top: 20px;
            padding: 15px;
            border-radius: 8px;
            display: none;
        }
        .status.info {
            background: #e3f2fd;
            color: #1976d2;
            border-left: 4px solid #1976d2;
        }
        .status.success {
            background: #e8f5e9;
            color: #388e3c;
            border-left: 4px solid #388e3c;
        }
        .status.error {
            background: #ffebee;
            color: #d32f2f;
            border-left: 4px solid #d32f2f;
        }
        .progress {
            margin-top: 15px;
            height: 6px;
            background: #e0e0e0;
            border-radius: 3px;
            overflow: hidden;
            display: none;
        }
        .progress-bar {
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            width: 0%;
            transition: width 0.3s;
        }
        .download-btn {
            margin-top: 15px;
            background: #4caf50;
            display: none;
        }
        .download-btn:hover {
            box-shadow: 0 10px 20px rgba(76, 175, 80, 0.4);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📝 Notion 转 Word 转换器</h1>
        <p class="subtitle">将公开的 Notion 页面转换为 Word 文档，无需 API Key</p>
        
        <form id="convertForm">
            <div class="input-group">
                <label for="url">🔗 Notion 页面 URL</label>
                <input type="text" id="url" name="url" placeholder="https://www.notion.so/your-public-page" required>
            </div>
            
            <div class="input-group">
                <label for="timeout">⏱️ 超时时间 (毫秒)</label>
                <input type="number" id="timeout" name="timeout" value="60000" min="10000" step="5000">
            </div>
            
            <div class="checkbox-group">
                <input type="checkbox" id="showBrowser" name="showBrowser">
                <label for="showBrowser" style="margin-bottom: 0;">显示浏览器窗口 (调试模式)</label>
            </div>
            
            <button type="submit" id="convertBtn">开始转换</button>
        </form>
        
        <div class="progress" id="progress">
            <div class="progress-bar" id="progressBar"></div>
        </div>
        
        <div class="status" id="status"></div>
        
        <button class="download-btn" id="downloadBtn" onclick="downloadFile()">📥 下载 Word 文档</button>
    </div>

    <script>
        let downloadData = null;

        document.getElementById('convertForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const url = document.getElementById('url').value;
            const timeout = document.getElementById('timeout').value;
            const showBrowser = document.getElementById('showBrowser').checked;
            const statusDiv = document.getElementById('status');
            const progressDiv = document.getElementById('progress');
            const progressBar = document.getElementById('progressBar');
            const downloadBtn = document.getElementById('downloadBtn');
            const convertBtn = document.getElementById('convertBtn');
            
            // 重置状态
            downloadBtn.style.display = 'none';
            statusDiv.style.display = 'none';
            progressDiv.style.display = 'block';
            convertBtn.disabled = true;
            
            // 显示进度
            progressBar.style.width = '30%';
            showStatus('info', '🚀 正在启动浏览器并加载页面...');
            
            try {
                const response = await fetch('/convert', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url, timeout: parseInt(timeout), show_browser: showBrowser })
                });
                
                progressBar.style.width = '70%';
                
                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || '转换失败');
                }
                
                progressBar.style.width = '100%';
                
                downloadData = await response.blob();
                showStatus('success', '🎉 转换成功！点击下方按钮下载文档。');
                downloadBtn.style.display = 'block';
                
            } catch (error) {
                showStatus('error', '❌ ' + error.message);
            } finally {
                convertBtn.disabled = false;
                setTimeout(() => {
                    progressDiv.style.display = 'none';
                    progressBar.style.width = '0%';
                }, 500);
            }
        });
        
        function showStatus(type, message) {
            const statusDiv = document.getElementById('status');
            statusDiv.className = 'status ' + type;
            statusDiv.textContent = message;
            statusDiv.style.display = 'block';
        }
        
        function downloadFile() {
            if (downloadData) {
                const url = window.URL.createObjectURL(downloadData);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'notion_export.docx';
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/convert', methods=['POST'])
def convert():
    try:
        data = request.json
        url = data.get('url')
        timeout = data.get('timeout', 30000)
        show_browser = data.get('show_browser', False)
        
        if not url:
            return jsonify({'error': '请提供 Notion 页面 URL'}), 400
        
        # 抓取页面
        scraper = NotionScraper(headless=not show_browser)
        html_content = scraper.scrape_page(url, timeout=timeout)
        
        # 转换为 Word
        converter = NotionToWordConverter()
        output_stream = io.BytesIO()
        converter.convert(html_content, output_stream)
        output_stream.seek(0)
        
        return send_file(
            output_stream,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            as_attachment=True,
            download_name='notion_export.docx'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    import webbrowser
    import threading
    
    def open_browser():
        """延迟打开浏览器"""
        import time
        time.sleep(1.5)  # 等待服务器启动
        webbrowser.open('http://localhost:5000')
    
    print("=" * 60)
    print("  📝 Notion 转 Word 转换器 (Flask 版)")
    print("=" * 60)
    print("\n✅ 服务器启动成功！")
    print("🌐 正在打开浏览器...")
    print("🌐 如果浏览器未自动打开，请手动访问: http://localhost:5000")
    print("\n按 Ctrl+C 停止服务器\n")
    
    # 在后台线程中打开浏览器
    threading.Thread(target=open_browser, daemon=True).start()
    
    app.run(debug=False, host='0.0.0.0', port=5000)
