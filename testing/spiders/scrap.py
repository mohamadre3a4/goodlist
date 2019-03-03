import scrapy
from scrapy.crawler import CrawlerProcess
import csv


class Goodreads(scrapy.Spider):
    name='good'
    def start_requests(self):
        urls = []

        link = 'https://www.goodreads.com/list/show/23425._'
        page = 11
        # add urls of pages in this case 11 pages
        for i in range(page):
            urls.append(link+'?page='+str(i+1))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_front)

    def parse_front(self,response):
        booklinks = response.xpath('//a[@class="bookTitle"]/@href').extract()
        for booklink in booklinks:
            yield response.follow(url ='https://www.goodreads.com/'+booklink, callback=self.parse_page)

    def parse_page(self,response):

        book_title = response.xpath('//h1[@id="bookTitle"]/text()').extract_first().strip()
        ratings = response.xpath('//meta[@itemprop="ratingCount"]/@content').extract_first()
        reviews = response.xpath('//meta[@itemprop="reviewCount"]/@content').extract_first()
        rate_val = response.xpath('//span[@itemprop="ratingValue"]/text()').extract_first().strip()
        isbn = response.xpath('//div[@id="bookDataBox"]/div[2]/div[2]/text()').extract_first().strip()
        
        yield {'isbn':isbn, 'title':book_title, 'rating_count':ratings, 'reviews':reviews,'rating_value':rate_val}
    


        
