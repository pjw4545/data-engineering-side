
import sqlite3

def add_sentiment_columns(db_path):
    """데이터베이스에 감성 분석 컬럼 추가"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("ALTER TABLE articles ADD COLUMN sentiment_polarity REAL")
        print("Added sentiment_polarity column.")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("sentiment_polarity column already exists.")
        else:
            raise

    try:
        cursor.execute("ALTER TABLE articles ADD COLUMN sentiment_subjectivity REAL")
        print("Added sentiment_subjectivity column.")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("sentiment_subjectivity column already exists.")
        else:
            raise
            
    conn.commit()
    conn.close()

if __name__ == "__main__":
    db_path = 'news.db'
    add_sentiment_columns(db_path)
    print(f"Database schema updated for {db_path}")
