# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TencentItem(scrapy.Item):
    # 职位名称
    positionName = scrapy.Field()

    # 职位类别
    positionType = scrapy.Field()

    # 工作地点
    workLocation = scrapy.Field()

    # 发布时间
    publishTime = scrapy.Field()
