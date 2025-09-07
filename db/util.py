import psycopg2
from typing import Optional, Dict, Any
from datetime import datetime

# Your Supabase connection string
CONN_STR = "postgresql://postgres.qsxuctlkevfprgyxkqbd:akuharusbisa@aws-1-us-east-2.pooler.supabase.com:5432/postgres"

def get_connection():
    """Get database connection"""
    return psycopg2.connect(CONN_STR)

def insert_kategori_putusan(title: str, link: str, count: int) -> Optional[int]:
    """
    Insert a new record into kategori_putusan table with duplicate prevention
    
    Args:
        title: The title of the category
        link: The link to the category
        count: The count value
        
    Returns:
        The ID of the inserted record, or None if failed/duplicate
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # Check for duplicate title
        check_query = "SELECT id FROM kategori_putusan WHERE title = %s"
        cur.execute(check_query, (title,))
        existing_record = cur.fetchone()
        
        if existing_record:
            print(f"⚠️  Duplicate category title found: '{title}' (ID: {existing_record[0]}). Skipping insertion.")
            cur.close()
            conn.close()
            return existing_record[0]  # Return existing ID
        
        # Insert new record
        query = """
        INSERT INTO kategori_putusan (title, link, count)
        VALUES (%s, %s, %s)
        RETURNING id;
        """
        
        cur.execute(query, (title, link, count))
        record_id = cur.fetchone()[0]
        
        conn.commit()
        cur.close()
        conn.close()
        
        print(f"✅ Successfully inserted kategori_putusan with ID: {record_id}")
        return record_id
        
    except Exception as e:
        print(f"❌ Failed to insert kategori_putusan: {e}")
        return None

def insert_putusan_ma(title: str, link: str, pengadilan: str, 
                     tanggal_register: str, tanggal_putus: str, 
                     tanggal_upload: str, views: str, category: str, downloads: str) -> Optional[int]:
    """
    Insert a new record into putusan_ma table with duplicate prevention
    
    Args:
        title: The title of the decision
        link: The link to the decision
        pengadilan: The court name
        tanggal_register: Registration date
        tanggal_putus: Decision date
        tanggal_upload: Upload date
        views: Number of views
        category: Category name
        downloads: Number of downloads
        
    Returns:
        The ID of the inserted record, or None if failed/duplicate
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # Check for duplicate title
        check_query = "SELECT id FROM putusan_ma WHERE title = %s"
        cur.execute(check_query, (title,))
        existing_record = cur.fetchone()
        
        if existing_record:
            print(f"⚠️  Duplicate title found: '{title}' (ID: {existing_record[0]}). Skipping insertion.")
            cur.close()
            conn.close()
            return existing_record[0]  # Return existing ID
        
        # Insert new record
        query = """
        INSERT INTO putusan_ma (title, link, pengadilan, tanggal_register, tanggal_putus, tanggal_upload, views, category, downloads)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
        """
        
        cur.execute(query, (title, link, pengadilan, tanggal_register, tanggal_putus, tanggal_upload, views, category, downloads))
        record_id = cur.fetchone()[0]
        
        conn.commit()
        cur.close()
        conn.close()
        
        print(f"✅ Successfully inserted putusan_ma with ID: {record_id}")
        return record_id
        
    except Exception as e:
        print(f"❌ Failed to insert putusan_ma: {e}")
        return None

def insert_kategori_putusan_batch(records: list) -> int:
    """
    Insert multiple records into kategori_putusan table in batch with duplicate prevention
    
    Args:
        records: List of tuples (title, link, count)
        
    Returns:
        Number of successfully inserted records
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        inserted_count = 0
        skipped_count = 0
        
        for title, link, count in records:
            # Check for duplicate title
            check_query = "SELECT id FROM kategori_putusan WHERE title = %s"
            cur.execute(check_query, (title,))
            existing_record = cur.fetchone()
            
            if existing_record:
                print(f"⚠️  Duplicate category title found: '{title}' (ID: {existing_record[0]}). Skipping.")
                skipped_count += 1
                continue
            
            # Insert new record
            query = """
            INSERT INTO kategori_putusan (title, link, count)
            VALUES (%s, %s, %s);
            """
            
            cur.execute(query, (title, link, count))
            inserted_count += 1
        
        conn.commit()
        cur.close()
        conn.close()
        
        print(f"✅ Batch insert completed: {inserted_count} inserted, {skipped_count} skipped")
        return inserted_count
        
    except Exception as e:
        print(f"❌ Failed to batch insert kategori_putusan: {e}")
        return 0

def insert_putusan_ma_batch(records: list) -> int:
    """
    Insert multiple records into putusan_ma table in batch with duplicate prevention
    
    Args:
        records: List of tuples (title, link, pengadilan, tanggal_register, tanggal_putus, tanggal_upload, views, category, downloads)
        
    Returns:
        Number of successfully inserted records
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        inserted_count = 0
        skipped_count = 0
        
        for title, link, pengadilan, tanggal_register, tanggal_putus, tanggal_upload, views, category, downloads in records:
            # Check for duplicate title
            check_query = "SELECT id FROM putusan_ma WHERE title = %s"
            cur.execute(check_query, (title,))
            existing_record = cur.fetchone()
            
            if existing_record:
                print(f"⚠️  Duplicate putusan title found: '{title}' (ID: {existing_record[0]}). Skipping.")
                skipped_count += 1
                continue
            
            # Insert new record
            query = """
            INSERT INTO putusan_ma (title, link, pengadilan, tanggal_register, tanggal_putus, tanggal_upload, views, category, downloads)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            
            cur.execute(query, (title, link, pengadilan, tanggal_register, tanggal_putus, tanggal_upload, views, category, downloads))
            inserted_count += 1
        
        conn.commit()
        cur.close()
        conn.close()
        
        print(f"✅ Batch insert completed: {inserted_count} inserted, {skipped_count} skipped")
        return inserted_count
        
    except Exception as e:
        print(f"❌ Failed to batch insert putusan_ma: {e}")
        return 0

def get_kategori_links():
    """
    Get all links from kategori_putusan table
    
    Returns:
        List of tuples (link, title) or empty list if failed
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        query = "SELECT link, title FROM kategori_putusan ORDER BY id"
        cur.execute(query)
        results = cur.fetchall()
        
        cur.close()
        conn.close()
        
        print(f"✅ Retrieved {len(results)} links from kategori_putusan")
        return results
        
    except Exception as e:
        print(f"❌ Failed to get kategori links: {e}")
        return []

def test_connection():
    """Test the database connection"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # Test query: check if tables exist
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        tables = cur.fetchall()
        
        print("✅ Connected to Supabase Postgres!")
        print("Available tables:", [table[0] for table in tables])
        
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        print("❌ Connection failed!")
        print("Error:", e)
        return False

# Example usage
if __name__ == "__main__":
    # Test connection
    test_connection()
    
    # Example single insert
    # insert_kategori_putusan("Test Category", "https://example.com", 100)
    # insert_putusan_ma("Test Decision", "https://example.com/decision", "MA", "2024-01-01", "2024-01-02", "2024-01-03")
    
    # Example batch insert
    # kategori_records = [
    #     ("Category 1", "https://example.com/1", 50),
    #     ("Category 2", "https://example.com/2", 75),
    # ]
    # insert_kategori_putusan_batch(kategori_records)
