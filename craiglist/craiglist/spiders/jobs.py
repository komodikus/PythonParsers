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

            yield scrapy.Request(link, callback=self.parse_listing,
                                 meta={
                                     'date': date,
                                     'link': link,
                                     'text': text
                                 })
        next_page_url = response.xpath('//*[@class="button next"]/@href').extract_first()

        if next_page_url:
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse)

    def parse_listing(self, response):
        date = response.meta['date'],
        link = response.meta['link']
        text = response.meta['text']

        compensation = response.xpath('//*[@class="attrgroup"]/span[1]/b/text()').extract_first()
        job_type = response.xpath('//*[@class="attrgroup"]/span[2]/b/text()').extract_first()

        images = response.xpath('//*[@id="thumbs"]//@src').extract()
        images = [image.replace("50x50c", "600x450") for image in images]

        job_desc = response.xpath('//*[@id="postingbody"]/text()').extract()
        yield {
            'date': date,
            'link': link,
            'text': text,
            'compensation': compensation,
            'job_type': job_type,
            'images': images,
            'job_desc': job_desc,
        }
