#!/usr/bin/env python3
"""
Test script to verify database integration with spiders
"""

import sys
import os

# Add the db directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'db'))
from util import test_connection, insert_kategori_putusan, insert_putusan_ma

def test_database_integration():
    """Test the database connection and insertion functions"""
    print("🔍 Testing database integration...")
    
    # Test connection
    if not test_connection():
        print("❌ Database connection failed!")
        return False
    
    print("\n📝 Testing insert functions...")
    
    # Test kategori_putusan insert
    print("Testing kategori_putusan insert...")
    kategori_id = insert_kategori_putusan(
        title="Test Category",
        link="https://example.com/test",
        count=100
    )
    
    if kategori_id:
        print(f"✅ kategori_putusan insert successful! ID: {kategori_id}")
    else:
        print("❌ kategori_putusan insert failed!")
        return False
    
    # Test putusan_ma insert
    print("Testing putusan_ma insert...")
    putusan_id = insert_putusan_ma(
        title="Test Decision",
        link="https://example.com/decision",
        pengadilan="MA",
        tanggal_register="2024-01-01",
        tanggal_putus="2024-01-02",
        tanggal_upload="2024-01-03"
    )
    
    if putusan_id:
        print(f"✅ putusan_ma insert successful! ID: {putusan_id}")
    else:
        print("❌ putusan_ma insert failed!")
        return False
    
    print("\n🎉 All database integration tests passed!")
    return True

if __name__ == "__main__":
    test_database_integration()
