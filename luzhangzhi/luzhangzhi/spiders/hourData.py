import scrapy


class HourdataSpider(scrapy.Spider):
    name = 'hourData'
    start_urls = ['http://117.78.34.39:7078/BigData/Main/']

    def parse(self, response):
        print("111111111111111111111111", response)
        pass
