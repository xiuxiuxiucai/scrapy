from selenium import webdriver
import time
import xlsxwriter
import re


# 搜索商品
def get_product(account, password):
    # 输入用户名
    print("正在登录...")
    driver.find_element_by_xpath("//input[@placeholder='请输入您的用户名']").send_keys(account)
    # 输入密码
    driver.find_element_by_xpath("//input[@placeholder='请输入您的密码']").send_keys(password)
    # 登录
    driver.find_element_by_xpath("//input[@value='登 录']").click()
    # 隐式等待
    driver.implicitly_wait(10)

    # 进入iframe
    print("正在进入iframe...")
    driver.get("http://117.78.34.39:7078/DataQuery/StationHistoryData")
    # 隐式等待vlue
    driver.implicitly_wait(10)

    # 选择站点
    print("正在设置站点、查询时间、查询项目、每页显示条数...")
    driver.find_element_by_xpath("//button[@onclick=\"toggleStation('stationDown')\"]").click()
    # 清空已选
    driver.find_element_by_xpath("//input[@value='清空已选']").click()
    # 选择国省道扬尘
    driver.find_element_by_xpath("//li[@onclick=\"getTheme('tab-1187',this)\"]").click()
    # 全选站点
    driver.find_element_by_xpath("//table[@id='tablist-1187']/thead/tr/th[@class='text-center']/input").click()
    # 确定
    driver.find_element_by_xpath("//input[@value='确定']").click()

    # 修改开始时间
    startDate = driver.find_element_by_xpath("//input[@id='startdate']")
    driver.execute_script("arguments[0].setAttribute(arguments[1],arguments[2])", startDate, "value", "2020-10-01 00:00")
    # 修改结束时间
    endDate = driver.find_element_by_xpath("//input[@id='enddate']")
    driver.execute_script("arguments[0].setAttribute(arguments[1],arguments[2])", endDate, "value", "2020-10-15 23:00")
    # 修改查询项目
    driver.find_element_by_xpath("//input[@map='PM25_V']").click()
    driver.find_element_by_xpath("//input[@map='SO2_V']").click()
    driver.find_element_by_xpath("//input[@map='NO2_V']").click()
    driver.find_element_by_xpath("//input[@map='CO_V']").click()
    driver.find_element_by_xpath("//input[@map='O3_V']").click()
    driver.find_element_by_xpath("//input[@map='VAL8_V']").click()
    driver.find_element_by_xpath("//input[@map='VAL3_V']").click()
    time.sleep(1)
    # 查询 从而刷新查询项目
    driver.find_element_by_xpath("//button[@class='button button1'][1]").click()
    time.sleep(2)
    # 设置每页显示条数
    driver.find_element_by_xpath("//button[@class='btn btn-default dropdown-toggle']").click()
    page_num = driver.find_element_by_xpath("//ul[@class='dropdown-menu']/li[5]/a")
    driver.execute_script("arguments[0].innerHTML=30", page_num)
    time.sleep(1)
    # 查询
    print("正在查询...")
    page_num.click()
    time.sleep(3)

    html = driver.page_source
    data_text_one = re.findall(r"<tr data-index=\"1\">.*</tr>", html)
    print("aaaaa")
    print(data_text_one)

    data_text_two = re.findall(r"<td style=\"text-align: center; vertical-align: middle; \">.*</td>", data_text_one[0])
    print("bbbbb")
    print(data_text_two)


# 爬取数据
def parse_product():
    # 获取总页数
    page_total = int(driver.find_element_by_xpath("//li[@class='page-last']/a").text)
    print("数据总页数为：", page_total)

    # 创建一个工作簿并添加一张工作表
    workbook = xlsxwriter.Workbook("result.xlsx")
    worksheet = workbook.add_worksheet()

    # 从第一行开始
    row = 0

    i = 0
    while i < page_total:
        i += 1
        print("正在爬取第", i, "页数据")
        start = time.time()  # 记下开始时刻

        html = driver.page_source
        data_text_all = re.findall("", html)

        for data_text in data_text_all:
            worksheet.write_row(row, 0, str(data_text.text).split(" "))
            row += 1

        # # 获取表格数据
        # lis = driver.find_elements_by_css_selector('#AlarmInfo tbody tr')
        # # 解析
        # for li in lis:
        #     worksheet.write_row(row, 0, str(li.text).split(" "))
        #     row += 1
        #
        #     # name = li.find_elements_by_css_selector('td')[1].text
        #     # dataTime = li.find_elements_by_css_selector('td')[2].text
        #     # AQI = li.find_elements_by_css_selector('td')[3].text
        #     # PM10 = li.find_elements_by_css_selector('td')[4].text
        #     #
        #     # worksheet.write(row, 0, name)
        #     # worksheet.write(row, 1, dataTime)
        #     # worksheet.write(row, 2, AQI)
        #     # worksheet.write(row, 3, PM10)

        # 下一页
        driver.find_element_by_xpath("//li[@class='page-next']/a").click()
        time.sleep(2)
        end = time.time()  # 记下结束时刻
        print("用时：", end - start)

    workbook.close()


account = "hezexh"
password = "hz@123456"

print("正在打开浏览器...")

# 添加无头headless
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)

# 不添加无头headless
# driver = webdriver.Chrome()

print("正在打开网页...")
driver.get("http://117.78.34.39:7078/DataQuery/StationHistoryData")
driver.implicitly_wait(10)
get_product(account, password)
# parse_product()
