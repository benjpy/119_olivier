import os
from dotenv import load_dotenv
from serpapi import GoogleSearch

def search_artist_news():
    # Load environment variables
    load_dotenv()
    
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        print("Error: SERPAPI_API_KEY not found in .env file")
        return

    # Read artist name from file
    try:
        with open("artist.txt", "r") as f:
            artist_name = f.read().strip()
    except FileNotFoundError:
        print("Error: artist.txt not found")
        return

    if not artist_name:
        print("Error: artist.txt is empty")
        return

    print(f"Searching news for: {artist_name}...")

    # Configure search
    params = {
        "engine": "google_news",
        "q": artist_name,
        "tbs": "qdr:m",  # Past month (30 days)
        "api_key": api_key
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        news_results = results.get("news_results", [])

        # Write results to file
        with open("results.txt", "w") as f:
            if not news_results:
                f.write(f"No news found for {artist_name} in the past 30 days.\n")
                print("No results found.")
            else:
                f.write(f"News results for {artist_name} (Past 30 Days):\n\n")
                for i, news in enumerate(news_results, 1):
                    title = news.get("title", "No Title")
                    link = news.get("link", "No Link")
                    date = news.get("date", "No Date")
                    source = news.get("source", {}).get("name", "Unknown Source")
                    
                    f.write(f"{i}. {title}\n")
                    f.write(f"   Source: {source} - {date}\n")
                    f.write(f"   Link: {link}\n\n")
                
                print(f"Success! {len(news_results)} results written to results.txt")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    search_artist_news()
