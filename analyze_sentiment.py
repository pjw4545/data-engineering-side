
import sqlite3
from textblob import TextBlob

def analyze_sentiment_and_update_db(db_path):
    """데이터베이스의 기사 내용에 대해 감성 분석 수행 및 업데이트"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 감성 분석이 아직 수행되지 않은 기사만 가져오기
    cursor.execute("SELECT id, content FROM articles WHERE sentiment_polarity IS NULL")
    articles = cursor.fetchall()
    
    updated_count = 0
    for article_id, content in articles:
        if content:
            # TextBlob은 영어 감성 분석에 최적화되어 있습니다.
            # 한국어/일본어 기사의 경우 정확도가 낮을 수 있습니다.
            analysis = TextBlob(content)
            polarity = analysis.sentiment.polarity
            subjectivity = analysis.sentiment.subjectivity
            
            cursor.execute("UPDATE articles SET sentiment_polarity = ?, sentiment_subjectivity = ? WHERE id = ?",
                           (polarity, subjectivity, article_id))
            updated_count += 1

    conn.commit()
    conn.close()
    print(f"Successfully analyzed sentiment for {updated_count} articles and updated the database.")

def main():
    """메인 실행 함수"""
    db_path = 'news.db'
    analyze_sentiment_and_update_db(db_path)
    print(f"Sentiment analysis completed for {db_path}")

if __name__ == "__main__":
    main()
