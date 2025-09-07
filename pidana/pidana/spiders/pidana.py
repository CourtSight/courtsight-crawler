import scrapy
import sys
import os

# Add the db directory to the path to import util
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'db'))
from util import insert_putusan_ma, get_kategori_links

class PutusanSpider(scrapy.Spider):
    name = "putusan_ma"
    
    def start_requests(self):
        """Generate requests from kategori_putusan database links"""
        try:
            # Get links from kategori_putusan table using helper function
            results = get_kategori_links()
            
            if not results:
                self.logger.warning("No links found in kategori_putusan table. Using fallback URL.")
                # Fallback to original URL if no database links
                yield scrapy.Request(
                    url="https://putusan3.mahkamahagung.go.id/direktori/index/kategori/pidana-khusus-1.html",
                    callback=self.parse
                )
                return
            
            self.logger.info(f"Found {len(results)} links in kategori_putusan table")
            
            # Generate requests for each link
            for link, title in results:
                self.logger.info(f"Scraping category: {title} - {link}")
                yield scrapy.Request(
                    url=link,
                    callback=self.parse,
                    meta={'category_title': title}
                )
                
        except Exception as e:
            self.logger.error(f"Failed to get links from database: {e}")
            # Fallback to original URL
            yield scrapy.Request(
                url="https://putusan3.mahkamahagung.go.id/direktori/index/kategori/pidana-khusus-1.html",
                callback=self.parse
            )

    def parse(self, response):
        # Get category title from meta (if available)
        category_title = response.meta.get('category_title', 'Unknown Category')
        self.logger.info(f"Parsing category: {category_title}")
        
        # Select all putusan blocks
        items = response.xpath('//div[contains(@class,"spost") and contains(@class,"clearfix")]')

        for item in items:
            # Extract main link & title
            link = item.xpath('.//strong/a/@href').get()
            title = item.xpath('normalize-space(.//strong/a/text())').get()

            # Extract tanggal register, putus, upload
            tanggal_register = item.xpath('normalize-space(.//div[@class="small"][2]/strong[contains(text(),"Register")]/following-sibling::text())').get()
            tanggal_putus = item.xpath('normalize-space(.//div[@class="small"][2]/strong[contains(text(),"Putus")]/following-sibling::text())').get()
            tanggal_upload = item.xpath('normalize-space(.//div[@class="small"][2]/strong[contains(text(),"Upload")]/following-sibling::text())').get()

            # Extract jumlah view & download
            views = item.xpath('.//strong[@title="Jumlah view"]/text()').get()
            downloads = item.xpath('.//strong[@title="Jumlah download"]/text()').get()

            # Extract pengadilan breadcrumb (first <a> inside .small)
            pengadilan = item.xpath('.//div[@class="small"][1]/a[2]/text()').get()

            # Prepare data for database insertion

            category_title = response.meta['category_title']
            data = {
                "title": title,
                "link": response.urljoin(link),
                "pengadilan": pengadilan,
                "tanggal_register": tanggal_register,
                "tanggal_putus": tanggal_putus,
                "tanggal_upload": tanggal_upload,
                "views": int(views) if views else 0,
                "downloads": int(downloads) if downloads else 0,
                "category": category_title,  # Add category information
            }

            # Insert into database
            if title and link:  # Only insert if we have required data
                record_id = insert_putusan_ma(
                    title=data["title"],
                    link=data["link"],
                    pengadilan=data["pengadilan"] or "",
                    tanggal_register=data["tanggal_register"] or "",
                    tanggal_putus=data["tanggal_putus"] or "",
                    tanggal_upload=data["tanggal_upload"] or "",
                    views=str(data["views"]) if data["views"] else "0",
                    downloads=str(data["downloads"]) if data["downloads"] else "0",
                    category=data["category"] or "",
                )
                
                if record_id:
                    data["db_id"] = record_id
                    self.logger.info(f"Processed putusan_ma record with ID: {record_id}")
                else:
                    self.logger.error(f"Failed to process putusan_ma record: {data['title']}")

            yield data
