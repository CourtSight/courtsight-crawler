#!/usr/bin/env python3
"""
Test script to verify the modified pidana spider works with database links
"""

import sys
import os

# Add the db directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'db'))
from util import test_connection, get_kategori_links, insert_kategori_putusan

def test_database_links():
    """Test getting links from kategori_putusan table"""
    print("🔍 Testing database links functionality...")
    
    # Test connection
    if not test_connection():
        print("❌ Database connection failed!")
        return False
    
    # Test getting links
    print("\n📝 Testing get_kategori_links function...")
    links = get_kategori_links()
    
    if not links:
        print("⚠️  No links found in kategori_putusan table.")
        print("Adding some test data...")
        
        # Add some test data
        test_categories = [
            ("Pidana Khusus", "https://putusan3.mahkamahagung.go.id/direktori/index/kategori/pidana-khusus-1.html", 100),
            ("Pidana Umum", "https://putusan3.mahkamahagung.go.id/direktori/index/kategori/pidana-umum-1.html", 150),
        ]
        
        for title, link, count in test_categories:
            insert_kategori_putusan(title, link, count)
        
        # Try getting links again
        links = get_kategori_links()
    
    if links:
        print(f"✅ Successfully retrieved {len(links)} links:")
        for i, (link, title) in enumerate(links, 1):
            print(f"  {i}. {title}: {link}")
        return True
    else:
        print("❌ Failed to retrieve links!")
        return False

def test_spider_integration():
    """Test the spider integration"""
    print("\n🕷️  Testing spider integration...")
    
    try:
        # Import the spider
        sys.path.append(os.path.join(os.path.dirname(__file__), 'pidana', 'pidana', 'spiders'))
        from pidana import PutusanSpider
        
        spider = PutusanSpider()
        
        # Test start_requests method
        requests = list(spider.start_requests())
        
        if requests:
            print(f"✅ Spider generated {len(requests)} requests")
            for i, request in enumerate(requests[:3], 1):  # Show first 3
                category = request.meta.get('category_title', 'Unknown')
                print(f"  {i}. {category}: {request.url}")
            return True
        else:
            print("❌ Spider failed to generate requests!")
            return False
            
    except Exception as e:
        print(f"❌ Spider integration test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing modified pidana spider with database links...")
    
    # Test database links
    db_test = test_database_links()
    
    # Test spider integration
    spider_test = test_spider_integration()
    
    if db_test and spider_test:
        print("\n🎉 All tests passed! The spider is ready to use database links.")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
