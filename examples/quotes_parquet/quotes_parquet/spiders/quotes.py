import scrapy

from scrapy.loader import ItemLoader
from quotes_parquet.items import QuotesParquetItem


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "http://quotes.toscrape.com/page/1/",
        "http://quotes.toscrape.com/page/2/",
    ]

    def parse(self, response):
        for quote in response.css("div.quote"):
            l = ItemLoader(QuotesParquetItem(), response=response)
            l.add_css("text", "span.text::text")
            l.add_css("author", "small.author::text")
            l.add_css("tags", "div.tags a.tag::text")
            yield l.load_item()
