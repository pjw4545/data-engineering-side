
import json
import sqlite3

def create_database_and_table(db_path):
    """데이터베이스 연결 및 테이블 생성"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # articles 테이블 생성 (이미 존재하면 무시)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT,
            published_at TEXT,
            source TEXT
        )
    ''')
    
    conn.commit()
    return conn

def insert_data_from_json(conn, json_path):
    """JSON 파일에서 데이터를 읽어와 DB에 삽입"""
    cursor = conn.cursor()
    
    with open(json_path, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    inserted_count = 0
    for article in articles:
        # 중복 데이터 방지 (같은 제목과 출처의 기사는 무시)
        cursor.execute("SELECT id FROM articles WHERE title = ? AND source = ?", (article['title'], article['source']))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO articles (title, content, published_at, source) VALUES (?, ?, ?, ?)", 
                           (article['title'], article['content'], article['published_at'], article['source']))
            inserted_count += 1

    conn.commit()
    print(f"Successfully inserted {inserted_count} new articles into the database.")

def main():
    """메인 실행 함수"""
    db_path = 'news.db'
    json_path = 'news_articles.json'
    
    conn = create_database_and_table(db_path)
    insert_data_from_json(conn, json_path)
    conn.close()
    
    print(f"Data from {json_path} has been successfully saved to {db_path}")

if __name__ == "__main__":
    main()
