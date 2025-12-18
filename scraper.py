"""
Notion 页面爬虫模块
使用 Selenium 抓取公开的 Notion 页面内容
"""
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class NotionScraper:
    """Notion 页面爬虫类"""
    
    def __init__(self, headless: bool = True):
        """
        初始化爬虫
        
        Args:
            headless: 是否使用无头模式
        """
        self.headless = headless
    
    def scrape_page(self, url: str, timeout: int = 30000) -> str:
        """
        抓取 Notion 页面的完整 HTML 内容
        
        Args:
            url: Notion 页面 URL
            timeout: 页面加载超时时间（毫秒）
            
        Returns:
            页面的完整 HTML 内容
            
        Raises:
            Exception: 页面加载失败或无法访问
        """
        # 配置 Chrome 选项
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        # 初始化 WebDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(timeout / 1000)  # 转换为秒
        
        try:
            # 访问页面
            driver.get(url)
            
            # 增加等待时间并使用更宽松的条件
            wait = WebDriverWait(driver, max(60, timeout / 1000))  # 至少60秒
            
            # 等待页面基本加载完成
            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.notion-page-content')))
            except:
                # 如果找不到标准选择器，尝试等待任何 notion 相关元素
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[class*="notion"]')))
            
            # 额外等待确保内容渲染
            time.sleep(3)
            
            # 滚动到底部以触发懒加载
            self._scroll_to_bottom(driver)
            
            # 再等待一下让图片加载
            time.sleep(3)
            
            # 获取完整 HTML
            html_content = driver.page_source
            
            return html_content
            
        except Exception as e:
            raise Exception(f"抓取页面失败: {str(e)}")
        
        finally:
            driver.quit()
    
    def _scroll_to_bottom(self, driver, scroll_pause: float = 0.5):
        """
        滚动到页面底部以触发懒加载
        
        Args:
            driver: Selenium WebDriver 对象
            scroll_pause: 每次滚动后的暂停时间（秒）
        """
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        while True:
            # 滚动到底部
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # 等待新内容加载
            time.sleep(scroll_pause)
            
            # 计算新的滚动高度
            new_height = driver.execute_script("return document.body.scrollHeight")
            
            # 如果高度没有变化，说明已经到底
            if new_height == last_height:
                break
                
            last_height = new_height
