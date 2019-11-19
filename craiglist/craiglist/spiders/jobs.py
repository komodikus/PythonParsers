# -*- coding: utf-8 -*-
import scrapy


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['philadelphia.craigslist.org']
    start_urls = ['https://philadelphia.craigslist.org/search/egr']

    def parse(self, response):
        listings = response.xpath('//li[@class="result-row"]')

        for listing in listings:
            date = listing.xpath('.//*[@class="result-date"]/@datetime').extract_first()
            link = listing.xpath('.//a[@class="result-title hdrlnk"]/@href').extract_first()
            text = listing.xpath('.//a[@class="result-title hdrlnk"]/text()').extract_first()

            yield {
                'date': date,
                'link': link,
                'text': text
            }
        next_page_url = response.xpath('//*[@class="button next"]/@href').extract_first()
        print('*'*20)
        print(next_page_url)
        print('*'*20)
        if next_page_url:
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse)
