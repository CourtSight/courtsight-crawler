# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
import sys
from itemadapter import ItemAdapter

# Add the db directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'db'))
from util import insert_informasi_putusan


class PidanaPipeline:
    def process_item(self, item, spider):
        return item


class InformasiPutusanPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Convert the item to a dictionary
        item_dict = dict(adapter)
        
        # Insert into database
        record_id = insert_informasi_putusan(item_dict)
        
        if record_id:
            spider.logger.info(f"Successfully processed item with ID: {record_id}")
        else:
            spider.logger.warning(f"Failed to process item: {item_dict.get('url', 'Unknown URL')}")
        
        return item
