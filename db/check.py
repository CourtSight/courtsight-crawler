import psycopg2
from urllib.parse import urlparse

# Your Supabase connection string

conn_str = "postgresql://postgres.qsxuctlkevfprgyxkqbd:akuharusbisa@aws-1-us-east-2.pooler.supabase.com:5432/postgres"

try:
    # Connect to Supabase Postgres
    conn = psycopg2.connect(conn_str)
    cur = conn.cursor()

    # Test query: fetch current time from Supabase server
    cur.execute("SELECT * FROM putusan_ma;")
    result = cur.fetchone()

    print("✅ Connected to Supabase Postgres!")
    print(result)

    cur.close()
    conn.close()
except Exception as e:
    print("❌ Connection failed!")
    print("Error:", e)
