import scrapy
from Tencent.items import TencentItem


class TencentSpider(scrapy.Spider):
    name = 'tencent'

    start_urls = ["https://www.bilibili.com/ranking"]

    def parse(self, response):

        print("111111111111111111111111111")

        titles = response.xpath("//a[@class='title']/text()").extract()
        urls = response.xpath("//a[@class='title']/@href").extract()
        watchNums = response.xpath("//span[@class='data-box']/i[@class='b-icon play']/../text()").extract()
        fires = response.xpath("//span[@class='data-box']/i[@class='b-icon view']/../text()").extract()
        authors = response.xpath("//span[@class='data-box']/i[@class='b-icon author']/../text()").extract()

        i = 0
        for title in titles:
            item = TencentItem()

            # 标题
            item["title"] = title
            print("2222222222222222222222", item["title"])
            # 链接
            item["url"] = urls[i]
            # 播放量
            item["watchNum"] = watchNums[i]
            # 弹幕
            item["fire"] = fires[i]
            # 作者
            item["author"] = authors[i]

            i += 1
            yield item
