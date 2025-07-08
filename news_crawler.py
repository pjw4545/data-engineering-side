import requests
import json
import datetime
import feedparser

# 사용자로부터 제공받은 News API 키
import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def search_news_api(query, language, api_key, count=5):
    """News API를 통해 특정 키워드로 뉴스 검색하기"""
    # ... (이전과 동일, 변경 없음)
    articles_to_return = []
    try:
        url = f"https://newsapi.org/v2/everything"
        params = {
            "q": query,
            "language": language,
            "apiKey": api_key,
            "pageSize": count,
            "sortBy": "publishedAt"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        print(f"Successfully fetched {len(data.get('articles', []))} articles from News API for query '{query}'.")

        for article in data.get("articles", []):
            content = article.get('description') or article.get('content') or ''
            pub_date_str = article.get('publishedAt', '')
            pub_date = datetime.datetime.fromisoformat(pub_date_str.replace('Z', '+00:00')).strftime('%Y-%m-%d')

            articles_to_return.append({
                "title": article.get('title'),
                "content": content,
                "published_at": pub_date,
                "source": article.get('source', {}).get('name')
            })
        return articles_to_return
    except Exception as e:
        print(f"Error fetching news from News API for query '{query}': {e}")
        return []

def get_news_from_rss(rss_url, source_name, count=5):
    """RSS 피드를 통해 뉴스 기사 가져오기 (안정성 개선)"""
    articles_to_return = []
    try:
        feed = feedparser.parse(rss_url)
        print(f"Successfully fetched {len(feed.entries)} entries from RSS feed: {source_name}")
        
        for entry in feed.entries[:count]:
            # 날짜 정보가 없을 경우를 대비하여 예외 처리
            date_tuple = None
            if hasattr(entry, 'published_parsed'):
                date_tuple = entry.published_parsed
            elif hasattr(entry, 'updated_parsed'):
                date_tuple = entry.updated_parsed
            
            if date_tuple:
                pub_date = datetime.datetime(*date_tuple[:6]).strftime('%Y-%m-%d')
            else:
                print(f"Warning: Could not find date for an entry from {source_name}. Skipping.")
                continue # 날짜 정보가 없으면 해당 기사는 건너뜀

            articles_to_return.append({
                "title": entry.title,
                "content": entry.summary,
                "published_at": pub_date,
                "source": source_name
            })
        return articles_to_return
    except Exception as e:
        print(f"Error fetching news from RSS feed {rss_url}: {e}")
        return []

def main():
    """메인 실행 함수"""
    all_articles = []

    # 1. News API로 한국 뉴스 수집
    kr_articles = search_news_api(query='한국', language='ko', api_key=NEWS_API_KEY, count=5)
    all_articles.extend(kr_articles)

    # 2. News API로 미국 뉴스 수집
    us_articles = search_news_api(query='united states', language='en', api_key=NEWS_API_KEY, count=5)
    all_articles.extend(us_articles)

    # 3. RSS 피드로 일본 뉴스 수집
    jp_rss_feeds = {
        "NHK": "https://www.nhk.or.jp/rss/news/cat0.xml",
        "Asahi Shimbun": "https://www.asahi.com/rss/asahi/newsheadlines.rdf"
    }
    for name, url in jp_rss_feeds.items():
        jp_articles = get_news_from_rss(url, name, count=2) # 각 언론사별 2개씩
        all_articles.extend(jp_articles)

    # 수집된 모든 기사를 JSON 파일로 저장
    with open('news_articles.json', 'w', encoding='utf-8') as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=4)

    print(f"\nTotal {len(all_articles)} articles have been collected and saved to news_articles.json")

if __name__ == "__main__":
    main()
