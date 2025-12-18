#!/usr/bin/env python3
"""
Notion 转 Word 转换器
将公开的 Notion 页面转换为 Word 文档
"""
import sys
import argparse
from pathlib import Path

# 修复 Python 3.13+ 在 Windows 上的 asyncio 兼容性问题
if sys.platform == 'win32' and sys.version_info >= (3, 8):
    import asyncio
    try:
        if hasattr(asyncio, 'WindowsSelectorEventLoopPolicy'):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except Exception:
        pass

from scraper import NotionScraper
from converter import NotionToWordConverter


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='将公开的 Notion 页面转换为 Word 文档',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py https://www.notion.so/your-page-id
  python main.py https://www.notion.so/your-page-id -o output.docx
  python main.py https://www.notion.so/your-page-id --show-browser
        """
    )
    
    parser.add_argument(
        'url',
        help='Notion 页面的公开 URL'
    )
    
    parser.add_argument(
        '-o', '--output',
        default='notion_export.docx',
        help='输出的 Word 文件名 (默认: notion_export.docx)'
    )
    
    parser.add_argument(
        '--show-browser',
        action='store_true',
        help='显示浏览器窗口（调试用）'
    )
    
    parser.add_argument(
        '--timeout',
        type=int,
        default=30000,
        help='页面加载超时时间（毫秒，默认: 30000）'
    )
    
    args = parser.parse_args()
    
    # 验证 URL
    if not args.url.startswith('http'):
        print("❌ 错误: 请提供有效的 URL")
        sys.exit(1)
    
    print(f"🚀 开始转换 Notion 页面...")
    print(f"📄 URL: {args.url}")
    
    try:
        # 步骤 1: 抓取页面
        print("\n⏳ 正在抓取页面内容...")
        scraper = NotionScraper(headless=not args.show_browser)
        html_content = scraper.scrape_page(args.url, timeout=args.timeout)
        print("✅ 页面抓取成功")
        
        # 步骤 2: 转换为 Word
        print("\n⏳ 正在生成 Word 文档...")
        converter = NotionToWordConverter()
        converter.convert(html_content, args.output)
        print(f"✅ Word 文档生成成功")
        
        # 显示结果
        output_path = Path(args.output).absolute()
        print(f"\n🎉 转换完成!")
        print(f"📁 文件位置: {output_path}")
        
        if converter.image_count > 0:
            print(f"🖼️  已处理 {converter.image_count} 张图片")
        
    except Exception as e:
        print(f"\n❌ 转换失败: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
