# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ShowspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    date = scrapy.Field()
    time = scrapy.Field()
    venue = scrapy.Field()
    artist = scrapy.Field()
    post = scrapy.Field()
    source = scrapy.Field()
