import requests
import os

SERP_API_KEY = os.getenv('SERP_API_KEY')
keyword = "kampung inggris"
domain = "kampunginggris.id"
page = 0
max_pages = 5

while page < max_pages:
    url = f"https://serpapi.com/search.json?engine=google&q={keyword}&api_key={SERP_API_KEY}&start={page * 10}&location=Indonesia&hl=id&device=mobile"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        break
    
    results = response.json().get("organic_results", [])
    
    if results:
        for rank, result in enumerate(results, start=(page * 10) + 1):
            if domain in result.get("link", ""):
                print(f"Found {domain} at position {rank} on page {page + 1}")
                break
    else:
        print("No results found on this page.")

    if len(results) < 10:
        break
    page += 1
