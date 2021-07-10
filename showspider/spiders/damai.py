import scrapy
import datetime
from showspider.items import ShowspiderItem

class DamaiSpider(scrapy.Spider):
    name = 'damai'
    
    url = 'http://damai.cn/'

    def start_requests(self):
        yield scrapy.Request(self.url, self.parse)

    def parse(self, response):
        banner = response.css('#slides')
        for link in banner.css('a::attr(href)').getall():
            yield scrapy.Request(link, self.parse_detail)

    def parse_detail(self, response):
        info = response.css('#staticDataDefault')

        id = info.re(r'\"itemId\":(.+?),').get()

        title = response.css('title::text').get()

        url = response.url

        date = info.re(r'\"showTime\":\"(.+?)\",').get()

        try:
            time = date[0:11]+date[-5:]
            time = datetime.datetime.strptime(time, "%Y.%m.%d %H:%M")
        except(ValueError):
            time = date[0:10]
            time = datetime.datetime.strptime(time, "%Y.%m.%d")

        venue = info.re(r'\"venueName\":\"(.+?)\",').get()
        city = info.re(r'\"venueCityName\":\"(.+?)\",').get()
        venue = city + venue

        artist = info.re(r'{\"title\":\"主要演员\",\"content\":\"(.+?)\"}').get()
        if artist == None:
            artist = '未知'

        item = ShowspiderItem()
        item['id'] = id
        item['title'] = title
        item['url'] = url
        item['date'] = date
        item['time'] = time
        item['venue'] = venue
        item['artist'] = artist
        yield item