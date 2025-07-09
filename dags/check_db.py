import sqlite3

def fetch_articles(db_path, limit=5):
    """데이터베이스에서 기사 조회"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute(f"SELECT title, source, published_at, sentiment_polarity, sentiment_subjectivity FROM articles LIMIT {limit}")
    rows = cursor.fetchall()
    
    conn.close()
    return rows

def main():
    """메인 실행 함수"""
    db_path = 'news.db'
    articles = fetch_articles(db_path)
    
    if articles:
        print("\n--- Top 5 Articles in news.db (with Sentiment) ---")
        for title, source, published_at, polarity, subjectivity in articles:
            print(f"Title: {title}\nSource: {source}\nPublished: {published_at}\nSentiment (Polarity/Subjectivity): {polarity:.2f}/{subjectivity:.2f}\n---")
    else:
        print("No articles found in the database.")

if __name__ == "__main__":
    main()
