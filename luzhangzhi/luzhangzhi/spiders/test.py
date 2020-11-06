from selenium import webdriver

# 添加无头headless
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(options=chrome_options)

# browser = webdriver.Chrome()

browser.get('http://www.baidu.com')

html=browser.page_source

print(html)