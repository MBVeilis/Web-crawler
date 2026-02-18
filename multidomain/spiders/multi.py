import scrapy


class MultiSpider(scrapy.Spider):
    name = "multi"
    allowed_domains = ["toscrape.com"]
    #start_urls = ["https://toscrape.com"]

    # starting URL (the first page of the Fantasy category)
    url: str = "https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html"

    # Modern async version of 'start_requests'
    async def start(self):
        # Yield our first request, sending the response to 'parse_listpage'
        yield scrapy.Request(self.url, callback=self.parse_listpage)

    # Handles the *category page*
    async def parse_listpage(self, response):
        # 1. get all product URLs using the selector we found
        product_urls = response.css("article.product_pod h3 a::attr(href)").getall()

        # 2. For each product URL, follow it and send the response to 'parse_book'
        for url in product_urls:
            yield response.follow(url, callback=self.parse_multi)

        # 3. Find the 'Next' page URL
        next_page_url = response.css("li.next a::attr(href)").get()

        # 4. If a 'Next' page exists, follow it and send the response
        if next_page_url:
            yield response.follow(next_page_url, callback=self.parse_listpage)

    # Handles the *Product page*
    @staticmethod
    async def parse_multi(response):
        # Yield a dictionary of the data we want
        yield {
            "name": response.css("h1::text").get(),
            "price": response.css("p.price_color::text").get(),
            "url": response.url
        }
