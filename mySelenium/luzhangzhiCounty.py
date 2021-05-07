from selenium import webdriver
import time
import xlsxwriter
import re
from tqdm import tqdm
import datetime
import calendar
from pykeyboard import PyKeyboard


# 搜索商品
def get_product():
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
    # 隐式等待
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
    time.sleep(2)

    # 修改查询时间
    if is_test:
        set_query_time("01", "03", True)
    else:
        set_query_time("01", "15", True)
    # 修改查询项目
    driver.find_element_by_xpath("//input[@map='PM25_V']").click()
    driver.find_element_by_xpath("//input[@map='SO2_V']").click()
    driver.find_element_by_xpath("//input[@map='NO2_V']").click()
    driver.find_element_by_xpath("//input[@map='CO_V']").click()
    driver.find_element_by_xpath("//input[@map='O3_V']").click()
    driver.find_element_by_xpath("//input[@map='VAL8_V']").click()
    driver.find_element_by_xpath("//input[@map='VAL3_V']").click()
    driver.find_element_by_xpath("//input[@map='TP_V']").click()
    driver.find_element_by_xpath("//input[@map='TD_V']").click()
    time.sleep(1)
    # 查询 从而刷新查询项目
    driver.find_element_by_xpath("//button[@class='button button1'][1]").click()
    time.sleep(2)
    # 设置每页显示条数
    driver.find_element_by_xpath("//button[@class='btn btn-default dropdown-toggle']").click()
    page_num = driver.find_element_by_xpath("//ul[@class='dropdown-menu']/li[5]/a")
    driver.execute_script("arguments[0].innerHTML=" + str(set_page_num), page_num)
    time.sleep(1)
    # 查询
    print("正在查询...")
    page_num.click()
    time.sleep(3)


# 修改查询时间
def set_query_time(begin_day, end_day, is_hours):
    # 判断查询小时数据还是查询天数据
    if is_hours:
        # 设置到第一页
        driver.find_element_by_xpath("//ul[@class='pagination']/li[2]/a").click()
        time.sleep(2)
        # 修改开始时间
        start_date = driver.find_element_by_xpath("//input[@id='startdate']")
        driver.execute_script("arguments[0].setAttribute(arguments[1],arguments[2])", start_date, "value",
                              data_time_str + begin_day + " 00:00")
        # 修改结束时间
        end_date = driver.find_element_by_xpath("//input[@id='enddate']")
        driver.execute_script("arguments[0].setAttribute(arguments[1],arguments[2])", end_date, "value",
                              data_time_str + end_day + " 23:00")
        time.sleep(2)
        # 查询
        driver.find_element_by_xpath("//button[@class='button button1'][1]").click()
        time.sleep(2)
    else:
        # 获取键盘对象
        k = PyKeyboard()
        # 设置到第一页
        driver.find_element_by_xpath("//ul[@class='pagination']/li[2]/a").click()
        time.sleep(2)
        # 修改时间类型
        driver.find_element_by_xpath("//a[@dateid='day']").click()
        time.sleep(2)
        # 修改开始时间
        start_date = driver.find_element_by_id("startdate")
        start_date.clear()
        start_date.click()
        time.sleep(2)
        k.type_string(data_time_str + begin_day)
        # 修改结束时间
        end_date = driver.find_element_by_id("enddate")
        end_date.clear()
        end_date.click()
        time.sleep(1)
        k.type_string(data_time_str + end_day)
        time.sleep(1)
        # 查询
        driver.find_element_by_xpath("//button[@class='button button1'][1]").click()
        time.sleep(2)


# 创建excel
def get_excel():
    # 创建一个工作簿并添加一张工作表
    workbook = xlsxwriter.Workbook("先河路长制国省道" + str(month) + "月份数据.xlsx")
    worksheet = workbook.add_worksheet()

    # 设置标题
    worksheet.write(0, 0, "name")
    worksheet.write(0, 1, "hours")
    worksheet.write(0, 2, "AQI")
    worksheet.write(0, 3, "PM10")
    worksheet.write(0, 4, "TP")
    worksheet.write(0, 5, "TD")

    # 获取数据并写入excel
    row = 1
    row = re_parse_product("国省道扬尘 小时数据 前半月,", worksheet, row)

    # 查询下一时间段数据
    if is_test:
        set_query_time("27", str(calendar.monthrange(year, month)[1]), True)
    else:
        set_query_time("16", str(calendar.monthrange(year, month)[1]), True)

    # 获取数据并写入excel
    hour_number = re_parse_product("国省道扬尘 小时数据 后半月,", worksheet, row)

    # 查询日数据
    set_query_time("01", str(calendar.monthrange(year, month)[1]), False)
    # 新建sheet页
    worksheet = workbook.add_worksheet()
    # 设置标题
    worksheet.write(0, 0, "name")
    worksheet.write(0, 1, "day")
    worksheet.write(0, 2, "AQI")
    worksheet.write(0, 3, "PM10")
    worksheet.write(0, 4, "TP")
    worksheet.write(0, 5, "TD")

    # 获取数据并写入excel
    day_number = re_parse_product("国省道扬尘 天数据,", worksheet, 1)

    # 关闭excel
    workbook.close()

    # 任务结束
    end = time.time()

    # 统计
    print("\n任务结束，共计用时：", round((end - start)/60, 2), "分钟")
    print("抓取小时数据条数：", hour_number - 1)
    print("抓取天数据条数：", day_number - 1)
    print()


# 正则表达式爬取数据
def re_parse_product(title, worksheet, row):
    # 获取总页数
    page_list = driver.find_elements_by_xpath("//ul[@class='pagination']/li")
    page_total = int(page_list[-2].text)
    print("\n" + title + "查询成功，数据总页数为：", page_total)

    # 显示进度条
    pbar = tqdm(total=page_total)

    i = 0
    while i < page_total:
        i += 1
        pbar.update(1)
        html = driver.page_source
        data_text_one = re.findall(r"<tr data-index=\"0\">.*</tr>", html)
        data_text_two = re.findall(r"(?<=<td style=\"text-align: center; vertical-align: middle; \">).*?(?=</td>)",
                                   data_text_one[0])

        # j来控制换行
        j = 0
        for data_text in data_text_two:
            if data_text == "-":
                data_text = ""
            if j != 0:
                worksheet.write(row, j - 1, data_text)
            j = j + 1
            if j == 7:
                row += 1
                j = 0

        # 下一页
        driver.find_element_by_xpath("//li[@class='page-next']/a").click()
        time.sleep(2)

    # 关闭进度条
    pbar.close()
    return row


# 常量属性设置
account = "hezexh"
password = "hz@123456"
set_page_num = 1000
# 如果开启测试，查询的数据量将大幅减少，从而提升测试效率，且不会关闭浏览器
is_test = False
# 循环次数，默认为1，它的值设为多少，就会生成多少次excel文档，且每次文档的数据月份加一
for_number = 1
# 获取前一月的数据
month = datetime.datetime.now().month - 1
year = datetime.datetime.now().year
# 获取特定月的数据
# month = 12
# year = 2020

i = 1
while i <= for_number:
    month = month + i - 1
    if month > 12:
        month = month - 12
        year = year + 1

    # 任务开始
    start = time.time()

    if month == 0:
        year = year - 1
        month = 12
    if month < 10:
        data_time_str = str(year) + "-0" + str(month) + "-"
    else:
        data_time_str = str(year) + "-" + str(month) + "-"

    print("正在打开浏览器...")

    # 不添加无头headless
    driver = webdriver.Chrome()

    print("正在打开网页...")
    driver.get("http://117.78.34.39:7078/DataQuery/StationHistoryData")
    driver.implicitly_wait(10)

    # 进入页面
    get_product()

    # 生成excel并写入数据
    get_excel()

    # 关闭浏览器
    if not is_test:
        driver.close()

    i = i + 1
