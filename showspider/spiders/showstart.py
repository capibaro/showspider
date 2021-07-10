import scrapy
import datetime
from showspider.items import ShowspiderItem

class ShowstartSpider(scrapy.Spider):
    name = 'showstart'

    venue_url = 'https://www.showstart.com/venue/list'

    city_urls = [
        "https://www.showstart.com/event/list?showStyle=1&cityCode=",
        "https://www.showstart.com/event/list?showStyle=2&cityCode=",
        "https://www.showstart.com/event/list?showStyle=3&cityCode=",
        "https://www.showstart.com/event/list?showStyle=4&cityCode=",
        "https://www.showstart.com/event/list?showStyle=6&cityCode=",
        "https://www.showstart.com/event/list?showStyle=10&cityCode=",
        "https://www.showstart.com/event/list?showStyle=11&cityCode=",
        "https://www.showstart.com/event/list?showStyle=12&cityCode=",
        "https://www.showstart.com/event/list?showStyle=23&cityCode=",
        "https://www.showstart.com/event/list?showStyle=24&cityCode=",
        "https://www.showstart.com/event/list?showStyle=25&cityCode=",
        "https://www.showstart.com/event/list?showStyle=26&cityCode=",
    ]

    domain_name = "https://www.showstart.com"
    
    def start_requests(self):
        yield scrapy.Request(self.venue_url, self.parse_city)

    def parse_city(self, response):
        filter_content = response.css('#__layout > section > main > div > section.filter-wrap > div')
        cities = filter_content.css('a::attr(href)')
        for city in cities:
            code_list = city.re(r'cityCode=(.+?)&t=')
            if len(code_list) != 0:
                city_code = code_list[0]
                for city_url in self.city_urls:
                    link = city_url + city_code
                    yield scrapy.Request(link, self.parse_page)

    def parse_page(self, response):
        el_pager = response.css('#__layout > section > main > div > div.el-pagination.is-background > ul > li::text').getall()
        if len(el_pager) != 0:
            count = int(el_pager[-1])
            for page in range(1, count+1):
                link = response.url + "&pageNo=" + str(page)
                yield scrapy.Request(link, self.parse_show)
    
    def parse_show(self, response):
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
            artist = artists[i][3:]
            date = dates[i][3:]
            time = date[0:20]
            time = datetime.datetime.strptime(time, '%Y/%m/%d %H:%M')
            venue = venues[i]
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