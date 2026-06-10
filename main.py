from apscheduler.schedulers.blocking import BlockingScheduler
from scraper import collect_all_news
from analyzer import analyze_article
from notifier import send_alert
from dotenv import load_dotenv
from datetime import datetime
import hashing
from database import engine, Base , get_db
from model import hash_title
db = get_db()
load_dotenv()

Base.metadata.create_all(engine)

# processed = set()
daily_newsapi_calls = 0      # track NewsAPI usage
last_reset_day = datetime.now().day

# def get_hash(text):
#     return hashlib.md5(text.encode()).hexdigest()

def reset_daily_counter():
    """resets counter at midnight"""
    global daily_newsapi_calls, last_reset_day
    today = datetime.now().day
    if today != last_reset_day:
        daily_newsapi_calls = 0
        last_reset_day = today
        print("Daily counters reset ✅")

def run_monitor():
    global daily_newsapi_calls

    reset_daily_counter()

    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Checking gold news...")
    print(f"NewsAPI calls today: {daily_newsapi_calls}/100")

    articles = collect_all_news(
        use_newsapi=daily_newsapi_calls < 90  # stop at 90 to be safe
    )

    daily_newsapi_calls += 1

    for article in articles:
        title_hash = hashing.hashing(article["title"])
        hashed_title = db.query(hash_title).filter(hash_title.title == title_hash).first()
        
        #article_hash = get_hash(article["title"])
        if hashed_title:
            continue #goes backt to the loop again
        #if it was break it will completely break the loop again

        new_entry = hash_title(title = title_hash)
        db.add(new_entry)
        db.commit()
        analysis = analyze_article(article)

        if analysis.get("relevant"):
            print(f"GOLD ALERT: {article['title'][:60]}")
            send_alert(article, analysis)
        else:
            print(f"Skip: {article['title'][:40]}")

# run immediately then every 20 minutes
run_monitor()

scheduler = BlockingScheduler()
scheduler.add_job(run_monitor, "interval", minutes=20)  # ← safe for 100/day limit

print("\nGold monitor running — checks every 20 minutes")
print("Press Ctrl+C to stop\n")

scheduler.start()