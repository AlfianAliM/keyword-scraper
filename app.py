import requests
from telegram import Bot
import asyncio
import os

# API keys
SERP_API_KEY = os.getenv('SERP_API_KEY')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

async def get_top_sites(keyword):
    top_sites = []
    page = 0  # Mulai dari halaman pertama
    max_pages = 2  # Ambil hingga 2 halaman pertama (20 hasil)
    
    while page < max_pages:
        # URL dengan perangkat mobile, lokasi Indonesia, dan bahasa Indonesia
        url = f"https://serpapi.com/search.json?engine=google&q={keyword}&api_key={SERP_API_KEY}&start={page * 10}&location=Indonesia&hl=id&device=mobile"
        
        response = requests.get(url)
        
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            return [f"Failed to fetch data from SERP API (status code {response.status_code})"]
        
        results = response.json()
        
        # Debugging: Log hasil JSON dari API
        print("API Response:", results)

        if "organic_results" not in results:
            print("No 'organic_results' in the response")
            return ["No organic results found"]
        
        results = results.get("organic_results", [])
        
        for rank, result in enumerate(results, start=(page * 10) + 1):
            site = result.get("link", "No link")
            title = result.get("title", "No title")
            top_sites.append(f"Rank {rank}: {title} - {site}")
        
        if len(results) < 10:
            break
        page += 1

    return top_sites

async def send_telegram_message(message):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        print(f"Error: {e}")

async def monitor_keywords(keywords):
    message = "Top 20 Keyword Ranking Report for 'kampung inggris':\n"
    for keyword in keywords:
        top_sites = await get_top_sites(keyword)
        if top_sites:
            for site in top_sites:
                message += f"{site}\n"
        else:
            message += f"No results found for keyword '{keyword}'.\n"
    
    await send_telegram_message(message)

# Keywords to monitor
keywords = ["kampung inggris"]

# Run the monitoring function
asyncio.run(monitor_keywords(keywords))