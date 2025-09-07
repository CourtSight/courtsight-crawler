import scrapy
import sys
import os

# Add the db directory to the path to import util
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'db'))
from util import insert_kategori_putusan

class PutusanSpider(scrapy.Spider):
    name = "pidana"
    start_urls = ["https://putusan3.mahkamahagung.go.id/direktori/index/kategori/pidana-khusus-1.html"]

    def parse(self, response):
        # Select the correct container
        elements = response.xpath(
            '(//*[@aria-labelledby="headingOne"])[2]//div[contains(@class,"card-body")]//div[contains(@class,"form-check")]'
        )

        for el in elements:
            link = el.xpath('.//p[@class="card-text"]/a/@href').get()
            title = el.xpath('normalize-space(.//p[@class="card-text"]/a/text()[1])').get()
            count = el.xpath('.//p[@class="card-text"]/a/span/text()').get()

            # Prepare data for database insertion
            data = {
                "link": response.urljoin(link),
                "title": title,
                "count": int(count) if count else 0
            }

            # Insert into database
            if title and link:  # Only insert if we have required data
                record_id = insert_kategori_putusan(
                    title=data["title"],
                    link=data["link"],
                    count=data["count"]
                )
                
                if record_id:
                    data["db_id"] = record_id
                    self.logger.info(f"Processed kategori_putusan record with ID: {record_id}")
                else:
                    self.logger.error(f"Failed to process kategori_putusan record: {data['title']}")

            yield data
