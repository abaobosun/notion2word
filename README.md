# Notion 转 Word 转换器

将公开的 Notion 页面转换为 Microsoft Word 文档（.docx）的工具。

## ✨ 特性

- ✅ 无需 Notion API Token，直接转换公开页面
- ✅ 支持标题、段落、列表、图片等常见元素
- ✅ 保留文本格式（粗体、斜体、下划线等）
- ✅ 自动处理懒加载内容
- ✅ 命令行界面，简单易用

## 📋 系统要求

- Python 3.8+
- Windows / macOS / Linux
- Chrome 浏览器（Selenium 会自动管理 ChromeDriver）

## 🚀 安装

### 1. 克隆或下载项目

```bash
cd notion2Word
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

**注意**: 首次运行时，Selenium 会自动下载 ChromeDriver，请保持网络连接。

## 💡 使用方法

### 使用 Web 界面 (推荐)

启动简单易用的网页界面：

```bash
streamlit run app.py
```

或者直接双击运行文件夹中的 **`启动程序.bat`**。

### 命令行用法 (高级)

```bash
python main.py <Notion页面URL>
```

### 指定输出文件名

```bash
python main.py <Notion页面URL> -o 我的文档.docx
```

### 显示浏览器窗口（调试用）

```bash
python main.py <Notion页面URL> --show-browser
```

### 完整示例

```bash
python main.py https://www.notion.so/example-page-123456 -o output.docx
```

## 📖 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `url` | Notion 页面的公开 URL（必需） | - |
| `-o, --output` | 输出的 Word 文件名 | `notion_export.docx` |
| `--show-browser` | 显示浏览器窗口（调试用） | 隐藏 |
| `--timeout` | 页面加载超时时间（毫秒） | 30000 |

## 📝 注意事项

1. **页面必须公开**: 只能转换已公开分享的 Notion 页面
2. **图片有效期**: Notion 图片链接有时效性，建议转换后尽快查看
3. **复杂布局**: 分栏、数据库等复杂布局可能无法完美转换
4. **网络要求**: 需要稳定的网络连接以下载图片

## 🛠️ 技术架构

- **Playwright**: 无头浏览器，用于渲染和抓取 Notion 页面
- **BeautifulSoup4**: HTML 解析
- **python-docx**: Word 文档生成

## 🐛 常见问题

### 1. 提示"无法找到 Notion 内容区域"

- 检查 URL 是否正确
- 确认页面已设置为公开分享
- 尝试增加 `--timeout` 参数值

### 2. 图片无法加载

- Notion 图片链接可能已过期
- 检查网络连接是否正常

### 3. Playwright 安装失败

```bash
# 手动安装 Chromium
python -m playwright install chromium
```

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！
