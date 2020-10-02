# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TencentItem(scrapy.Item):
    # 标题
    title = scrapy.Field()

    # 链接
    url = scrapy.Field()

    # 播放量
    watchNum = scrapy.Field()

    # 弹幕
    fire = scrapy.Field()

    # 作者
    author = scrapy.Field()
