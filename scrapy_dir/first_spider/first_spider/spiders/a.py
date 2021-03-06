# -*- coding: utf-8 -*-
import scrapy
import csv

from lxml.html.clean import unicode
from scrapy.loader.processors import TakeFirst, Compose
from first_spider.items import FirstSpiderItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join

class A58comSpider(scrapy.Spider):
    name = 'lang8'
    #allowed_domains = ['58.com']
    #start_urls = ['http://58.com/']
    def start_requests(self):
        yield scrapy.Request('http://www.avlang8.com/thread-htm-fid-4.html',callback=self.parse)

    # def parse_chuzu(self,response):
    #     chuzu=response.xpath('//a[@tongji_tag="pc_home_dh_zf"]/@href').extract_first()
    #     yield scrapy.Request(response.urljoin(chuzu),callback=self.parse)


    def parse(self, response):

        li=response.xpath("//tr[@class='tr2']/following-sibling::*")
        page=response.xpath('//span[@class="pagesone"]/span/text()').extract_first()
        for url in li:
            l = FirstSpiderItemLoader(item=FirstSpiderItem(),response=response)
            #l = ItemLoader(item=FirstSpiderItem(), response=response)
            l.add_value('rent_type', page)
            phone=url.xpath('td[@class="tal"]/a[@class="subject"]/text()')
            l.add_value('rent_type', phone)
            #l.add_xpath('phone', 'td[@class="tal"]/a[@class="subject"]/text()')
            return l.load_item()

        next_page = response.xpath("//div[@class='cc']/span/div[@class='pages']/b/following-sibling::*")[0]
        if next_page is not None:
            next_page = response.urljoin(next_page.xpath("@href").extract_first())
            yield scrapy.Request(next_page,callback=self.parse)


    def parser_house_info(self,response):

        l = FirstSpiderItemLoader(item=FirstSpiderItem(),response=response)
        #l = ItemLoader(item=FirstSpiderItem(), response=response)
        l.add_xpath('phone', '//span[@class="house-chat-txt"]/text()')
        l.add_xpath('rent_type','//span[@class="c_333"]/text()')
        l.add_xpath('rent_money','//b[@class="f36"]/text()')
        #l.add_xpath('base_info','//ul[@class="f14"]/li')
        return l.load_item()

        # phone = response.xpath('//span[@class="house-chat-txt"]/text()').extract_first()
        # rent_money = response.xpath('//b[@class="f36"]/text()').extract_first()
        # rent_type = response.xpath('//span[@class="c_333"]/text()').extract_first()
        # base_info = response.xpath('//ul[@class="f14"]/li')
        # tmp = {}
        # for li in base_info:
        #     tmp_list = li.xpath('span/text()').extract()
        #     if len(tmp_list) >= 2 and len(tmp_list[0])>0 and len(tmp_list[1])>0:
        #         tmp[tmp_list[0]]=tmp_list[1]
        # yield {
        #     "phone":phone,
        #     "rent_money":rent_money,
        #     "rent_type":rent_type,
        #     "base_info":tmp,
        # }

class FirstSpiderItemLoader(ItemLoader):

    default_output_processor = TakeFirst()

    phone_in = MapCompose(unicode.title)
    phon_out = default_output_processor

    rent_money_in = MapCompose(unicode.strip)
    rent_money_out = default_output_processor

    rent_type_in = MapCompose(unicode.strip)
    rent_type_out = default_output_processor

    base_info_in = MapCompose(unicode.strip)
    base_info_out = default_output_processor


