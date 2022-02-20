import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class BestbuySpiderSpider(CrawlSpider):
    name = 'bestbuy_spider'
    allowed_domains = ['bestbuy.com']
    start_urls = ['https://www.bestbuy.com/site/shop/category']
    
    rules = (
        Rule(LinkExtractor(allow=('/abcat\d+'))),
        Rule(LinkExtractor(allow=('/site/shop/'))),
        Rule(LinkExtractor(allow=('pcmcat'), deny=('dynchar'))),
        Rule(LinkExtractor(allow=('p?skuId=')), callback='parse')
        
    )

    def parse(self, response):
        yield {
            'url': response.url,
            'name': response.xpath('//h1/text()').get(),
            'price': response.xpath('//div[contains(@class, "hero-price")]/span/text()').get(),
            'stars_and_reviews': response.xpath('//span[@class="popover-wrapper"]//div/p/text()').get(),
            'model': response.xpath('(//span[@class="product-data-value body-copy"])[1]/text()').get(),
            'sku': response.xpath('(//span[@class="product-data-value body-copy"])[2]/text()').get(),
            "categories": '|'.join(response.xpath('(//ol[@class="c-breadcrumbs-order-list"]//li/a)[position()>1 and position()<last()]/text()').getall())
        }
