import scrapy


class ListPidanaSpider(scrapy.Spider):
    name = "pidana"
    allowed_domains = ["putusan3.mahkamahagung.go.id"]
    start_urls = ["https://putusan3.mahkamahagung.go.id/direktori/index/kategori/pidana-khusus-1.html"]

    def parse(self, response):
        pass
