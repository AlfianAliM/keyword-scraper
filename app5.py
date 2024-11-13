import asyncio
from datetime import datetime
import requests
from telegram import Bot
import os
from dotenv import load_dotenv

load_dotenv()

SERP_API_KEY = os.getenv('SERP_API_KEY')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

async def check_ranking(keyword, domain):
    page = 0  
    max_pages = 5  
    
    while page < max_pages:
        url = f"https://serpapi.com/search.json?engine=google&q={keyword}&api_key={SERP_API_KEY}&start={page * 10}&location=Indonesia&hl=id&device=mobile"
        response = requests.get(url)
        
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            return f"Failed to fetch data for '{keyword}' (status code {response.status_code})"
        
        results = response.json().get("organic_results", [])
        
        for rank, result in enumerate(results, start=(page * 10) + 1):
            if domain in result.get("link", ""):
                return rank  
        
        if len(results) < 10:
            break
        page += 1

    return "Not in top 50"

async def send_telegram_message(message):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        print(f"Error: {e}")

async def monitor_keywords(keywords, domain):
    date_today = datetime.now().strftime("%Y-%m-%d")
    message = f"{date_today} {domain}\n"
    
    for keyword in keywords:
        rank = await check_ranking(keyword, domain)
        message += f"{keyword} : rank {rank}\n" if isinstance(rank, int) else f"{keyword} : {rank}\n"
    
    await send_telegram_message(message)

async def main():
    domains_and_keywords = [
        ("kampunginggris.id", ["kampung inggris", "kampung inggris pare"]),
        ("impacta.id", ["konsultan digital marketing", "konsultan marketing"]),
        ("nationaleyecenter.id", ["lasik", "operasi lasik", "lasik mata"]),
        ("jagonyakemasan.id", ["standing pouch"])
    ]
    
    while True:
        for domain, keywords in domains_and_keywords:
            await monitor_keywords(keywords, domain)
        
        # Set to 24 hours interval (in seconds)
        await asyncio.sleep(24 * 60 * 60) 

# Run the script
asyncio.run(main())
