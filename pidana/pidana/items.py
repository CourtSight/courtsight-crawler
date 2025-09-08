# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DeskripsiPutusanItem(scrapy.Item):
    hash_id = scrapy.Field()                 
    nomor = scrapy.Field()                   
    link_detail = scrapy.Field()             
    tingkat_proses = scrapy.Field()          
    klasifikasi = scrapy.Field()             
    kata_kunci = scrapy.Field()              
    lembaga_peradilan = scrapy.Field()       
    jenis_lembaga_peradilan = scrapy.Field() 
    hakim_ketua = scrapy.Field()             
    hakim_anggota = scrapy.Field()           
    panitera = scrapy.Field()                
    amar = scrapy.Field()                    
    amar_lainnya = scrapy.Field()            
    catatan_amar = scrapy.Field()            
    kaidah = scrapy.Field()                  
    abstrak = scrapy.Field()                 
    putusan_terkait = scrapy.Field()                 
    tahun = scrapy.Field()           
    tanggal_register = scrapy.Field()        
    tanggal_musyawarah = scrapy.Field()      
    tanggal_dibacakan = scrapy.Field()       
    jumlah_view = scrapy.Field()             
    jumlah_download = scrapy.Field()         
    link_zip = scrapy.Field()                
    link_pdf = scrapy.Field()                
    timestamp = scrapy.Field()       