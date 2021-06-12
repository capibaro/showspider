import scrapy
import re
import datetime
from scrapy_splash import SplashRequest
from showspider.items import ShowspiderItem

class ShowstartSpider(scrapy.Spider):
    name = 'showstart'
    city_url = "https://www.showstart.com/event/list?"
    domain_name = "https://www.showstart.com"
    start_urls = [
        'https://www.showstart.com/venue/list',
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.5})

    def parse(self, response):
        if response.url.find('venue') != -1:
            filter_content = response.css('#__layout > section > main > div > section.filter-wrap > div')
            cities = filter_content.css('a::attr(href)').getall()
            for city in cities:
                city_code = re.findall(r'list\?(.+?)&t', city)[0]
                link = self.city_url + city_code
                yield SplashRequest(link, self.parse, args={'wait':0.5})
                
        else:
            el_pager = response.css('#__layout > section > main > div > div.el-pagination.is-background > ul > li::text').getall()
            if len(el_pager) > 0:
                list_box = response.css('#__layout > section > main > div > div.list-box.clearfix')

                urls = list_box.css('a::attr(href)').getall()
                titles = list_box.css('div.title::text').getall()
                artists = list_box.css('div.artist::text').getall()
                dates = list_box.css('div.time::text').getall()
                venues = list_box.css('div.addr::text').getall()

                for i in range(0, len(urls)):
                    url = self.domain_name + urls[i]
                    id = url.split('/')[-1]
                    title = titles[i]
                    artist = artists[i]
                    date = dates[i]
                    time = date[3:20]
                    time = datetime.datetime.strptime(time, '%Y/%m/%d %H:%M')
                    venue = venues[i]
                    item = ShowspiderItem()
                    item['url'] = url
                    item['id'] = id
                    item['title'] = title
                    item['artist'] = artist
                    item['date'] = date
                    item['time'] = time
                    item['venue'] = venue
                    item['source'] = self.name
                    yield item
                
                if response.url.find('pageNo')==-1:
                    count = int(el_pager[-1])
                    for page in range(2, count+1):
                        link = response.url + "&pageNo=" + str(page)
                        yield SplashRequest(link, self.parse, args={'wait': 0.5})