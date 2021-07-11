import scrapy
import datetime
from showspider.items import ShowspiderItem

class ShowstartSpider(scrapy.Spider):
    name = 'showstart'

    url = "https://www.showstart.com/event/list?cityCode=%s&showStyle=%s"

    domain_name = "https://www.showstart.com"

    style_list = [1, 2, 3, 4, 6, 10, 11, 12, 23, 24, 25, 26]

    city_list = [10, 20, 21, 22, 23, 24, 28, 29, 371, 510, 512, 551, 571, 574, 591, 592, 731, 755]
    
    def start_requests(self):
        for style in self.style_list:
            for city in self.city_list:
                url = self.url % (str(city), str(style))
                yield scrapy.Request(url, self.parse_page)


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