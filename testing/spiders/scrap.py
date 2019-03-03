import scrapy
from scrapy.crawler import CrawlerProcess
import csv


class Goodreads(scrapy.Spider):
    name='good'
    def start_requests(self):
        urls = []

        # add urls of pages in this case 11 pages
        for i in range(1):
            urls.append('https://www.goodreads.com/list/show/128127._?page='+str(i+1))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_front)

    def parse_front(self,response):
        booklinks = response.xpath('//a[@class="bookTitle"]/@href').extract()
        for booklink in booklinks:
            yield response.follow(url ='https://www.goodreads.com/'+booklink, callback=self.parse_page)

    def parse_page(self,response):

        book_title = response.xpath('//h1[@id="bookTitle"]/text()')
        book_title_ext = book_title.extract_first()
        isbn = response.xpath('//div[@id="bookDataBox"]/div[2]/div[2]/text()')
        isbn_ext = isbn.extract_first()
        
        yield {'isbn':''.join(isbn_ext), 'title':''.join(book_title_ext)}
    


        
