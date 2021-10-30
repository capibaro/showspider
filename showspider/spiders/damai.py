import scrapy
import datetime
import json
from showspider.items import ShowspiderItem

class DamaiSpider(scrapy.Spider):
    name = 'damai'
    
    url = 'https://search.damai.cn/searchajax.html?ctl=%E6%BC%94%E5%94%B1%E4%BC%9A&tsg=0&order=1&pageSize=30&currPage='

    detail_url = 'https://detail.damai.cn/item.htm?id='

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS' : {
            'authority': 'search.damai.cn',
            'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="91", "Chromium";v="91"',
            'accept': 'application/json, text/plain, */*',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.67',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://search.damai.cn/search.htm',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        }
    }

    def start_requests(self):
        url = self.url + str(1)
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        result = json.loads(response.text)
        pageData = result.get('pageData')
        if pageData is not None:
            currentPage = pageData.get('currentPage')
            nextPage = pageData.get('nextPage')
            if (currentPage != nextPage):
                next_url = self.url + str(nextPage)
                yield scrapy.Request(next_url, self.parse)
            resultData = pageData.get('resultData')
            for show in resultData:
                id = show.get('projectid')
                url = self.detail_url + str(id)
                title = show.get('name')
                date = show.get('showtime')
                if date.find('-') != -1 or len(date) != 19:
                    time = date[0:10]
                    time = datetime.datetime.strptime(time, "%Y.%m.%d")
                else:
                    time = date[0:10] + date[-6:]
                    time = datetime.datetime.strptime(time, "%Y.%m.%d %H:%M")
                venuecity = show.get('venuecity')
                venue = show.get('venue')
                venue = venuecity + ' ' + venue
                artist = show.get('actors')[3:]
                post = show.get('verticalPic')
                item = ShowspiderItem()
                item['id'] = id
                item['url'] = url
                item['title'] = title
                item['date'] = date
                item['time'] = time
                item['venue'] = venue
                item['artist'] = artist
                item['post'] = post
                item['source'] = self.name
                yield item