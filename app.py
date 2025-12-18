import sys
import os
import io
import time

# 修复 Python 3.13+ 在 Windows 上的 asyncio 兼容性问题
if sys.platform == 'win32' and sys.version_info >= (3, 8):
    import asyncio
    try:
        if hasattr(asyncio, 'WindowsSelectorEventLoopPolicy'):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except Exception:
        pass

import streamlit as st
from scraper import NotionScraper
from converter import NotionToWordConverter
from playwright.sync_api import Error as PlaywrightError

# 设置页面配置
st.set_page_config(
    page_title="Notion 转 Word",
    page_icon="📝",
    layout="centered"
)

# 标题和简介
st.title("📝 Notion 转 Word 转换器")
st.markdown("""
    将公开的 Notion 页面直接转换为 Word 文档 (.docx)。
    只需粘贴 URL，无需 API Key。
""")

# 侧边栏配置
with st.sidebar:
    st.header("设置")
    show_browser = st.checkbox("显示浏览器 (调试模式)", value=False, help="勾选后将弹出浏览器窗口，可观察抓取过程")
    timeout = st.number_input("超时时间 (毫秒)", min_value=5000, value=30000, step=5000, help="页面加载超时时间，网速慢时可适当增加")

# 主界面输入
url = st.text_input("🔗 请输入 Notion 公开页面 URL", placeholder="https://www.notion.so/your-public-page")

# 转换按钮
if st.button("开始转换", type="primary", disabled=not url):
    if not url.startswith("http"):
        st.error("请输入有效的 URL (以 http 或 https 开头)")
    else:
        # 创建进度条和状态容器
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # 1. 启动爬虫
            status_text.info("🚀 正在启动浏览器...")
            progress_bar.progress(10)
            
            # 使用 session state 缓存爬取内容，避免重复爬取（可选，这里简化为每次转换都爬）
            scraper = NotionScraper(headless=not show_browser)
            
            status_text.info(f"⏳ 正在加载页面: {url}...")
            progress_bar.progress(30)
            
            # 执行爬取
            html_content = scraper.scrape_page(url, timeout=timeout)
            
            status_text.info("✅ 页面加载完成，正在解析内容...")
            progress_bar.progress(70)
            
            # 2. 转换为 Word
            status_text.info("📄 正在生成 Word 文档...")
            converter = NotionToWordConverter()
            
            # 使用 BytesIO 在内存中保存文件
            output_stream = io.BytesIO()
            converter.convert(html_content, output_stream)
            output_stream.seek(0)
            
            progress_bar.progress(100)
            status_text.success(f"🎉 转换成功！共处理 {converter.image_count} 张图片。")
            
            # 3. 提供下载
            st.download_button(
                label="📥 下载 Word 文档",
                data=output_stream,
                file_name="notion_export.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
            
        except PlaywrightError as e:
            status_text.error(f"❌ 浏览器错误: {str(e)}")
            st.warning("提示: 如果首次运行报错，请确保已运行 `playwright install chromium`")
        except Exception as e:
            status_text.error(f"❌ 转换失败: {str(e)}")
        finally:
            if 'progress_bar' in locals() and progress_bar:
                # 稍微延迟后清除进度条（或者保留显示完成状态）
                pass

# 页脚
st.markdown("---")
st.markdown("Made with ❤️ by Notion2Word | [GitHub](https://github.com/your-repo)")
