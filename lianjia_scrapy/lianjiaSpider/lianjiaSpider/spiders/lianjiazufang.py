# -*- coding: utf-8 -*-
import scrapy
from lianjiaSpider.items import LianjiaspiderItem
import re


class LianjiazufangSpider(scrapy.Spider):
    name = 'lianjiazufang'
    allowed_domains = ['lianjia.com']
    start_urls = []
    for i in range(1, 101):
        start_urls.append('https://nj.lianjia.com/zufang/pg'+str(i))

    def parse(self, response):
        house_list = response.xpath('//div[@class="content__list"]/div')
        for house in house_list:
            item = LianjiaspiderItem()
            item['title'] = house.xpath('./a[@class="content__list--item--aside"]/@title').extract_first()
            item['link'] = 'https://nj.lianjia.com' + house.xpath('./a[@class="content__list--item--aside"]/@href').extract_first()
            item['location'] = '.'.join(house.xpath('./div/p[2]/a/text()').extract())
            yield scrapy.Request(
                item['link'],
                callback=self.parse_detail,
                meta={'item': item}
            )

    def parse_detail(self, response):
        item = response.meta['item']
        item['rent'] = response.xpath('//p[@class="content__article__table"]/span[1]/text()').extract_first()
        item['apartment_layout'] = response.xpath('//p[@class="content__article__table"]/span[2]/text()').extract_first()
        item['area'] = response.xpath('//p[@class="content__article__table"]/span[3]/text()').extract_first()
        item['oriention'] = response.xpath('//p[@class="content__article__table"]/span[4]/text()').extract_first()
        publish_time = response.xpath('//div[@class="content__subtitle"]/text()').extract()[1]
        item['publish_time'] = publish_time.split(' ')[1]
        item['unit_price'] = response.xpath('//p[@class="content__aside--title"]/span/text()').extract_first()
        floor = response.xpath('//div[@class="content__article__info"]/ul/li[8]').extract_first()
        item['floor'] = re.findall('.*楼层：(.*).*</li>', floor)[0]
        yield item
        