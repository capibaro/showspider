import scrapy
import re
import json
import datetime
from showspider.items import ShowspiderItem

class GewaraSpider(scrapy.Spider):
    name = 'gewara'

    url = 'https://m.dianping.com/myshow/ajax/performances/%s;st=0;p=%s;s=10;tft=0?cityId=%s&sellChannel=7'
    
    detail_url = 'http://www.gewara.com/detail/'

    category_list = [1, 10]

    city_list = [1, 10, 20, 30, 40, 42, 44, 45, 50, 51, 52, 55, 56, 57, 59, 62, 66, 70, 73, 80]

    def start_requests(self):
        for category in self.category_list:
            for city in self.city_list:
                url = self.url % (str(category),'1',str(city))
                yield scrapy.Request(url, self.parse)

    def parse(self, response):
        result = json.loads(response.text)
        paging = result.get('paging')
        hasMore = paging.get('hasMore')
        if (hasMore == True):
            pageNo = paging.get('pageNo')
            pageNo = pageNo + 1
            next_url = re.sub("p=(.+?);","p="+str(pageNo)+";",response.url)
            yield scrapy.Request(next_url, self.parse)
        data = result.get('data')
        for show in data:
            id = show.get('performanceId')
            url = self.detail_url + str(id)
            title = show.get('name')
            artist = ''
            date = show.get('showTimeRange')
            if date.find('-') != -1 or date.find('/') != -1 or len(date) != 18:
                time = date.split(' ')[0]
                time = datetime.datetime.strptime(time, '%Y.%m.%d')
            else:
                time = date[:-3]
                time = datetime.datetime.strptime(time, '%Y.%m.%d %H:%M')
            venue = show.get('cityName') + ' ' + show.get('shopName')
            item = ShowspiderItem()
            item['id'] = id
            item['url'] = url
            item['title'] = title
            item['artist'] = artist
            item['date'] = date
            item['time'] = time
            item['venue'] = venue
            item['source'] = self.name
            yield item