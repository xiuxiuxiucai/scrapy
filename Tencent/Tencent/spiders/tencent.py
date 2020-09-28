import scrapy
from Tencent.items import TencentItem


class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['tencent.com']

    baseUrl = "https://careers.tencent.com/search.html?index="
    offset = 0
    start_urls = [baseUrl + str(offset)]

    def parse(self, response):

        print(response)

        positionNames = response.xpath("//h4[@class='recruit-title xh-highlight']")

        print(positionNames)

        for node in positionNames:
            item = TencentItem()
            # 职位名称
            item["positionName"] = node.extract()[0].encode("utf-8")
            print("1111111111111111111111111111111111", item["positionName"])
            # 职位类别
            item["positionType"] = node.xpath("../p[@class='recruit-tips']/span[3]").extract()[0].encode("utf-8")
            print(item["positionType"])
            # 工作地点
            item["workLocation"] = node.xpath("../p[@class='recruit-tips']/span[2]").extract()[0].encode("utf-8")
            print(item["workLocation"])
            # 发布时间
            item["publishTime"] = node.xpath("../p[@class='recruit-tips']/span[4]").extract()[0].encode("utf-8")
            print(item["publishTime"])

            yield item

        if self.offset < 3:
            self.offset += 1
            url = self.baseUrl + str(self.offset)
            yield scrapy.Request(url, callback = self.parse)
