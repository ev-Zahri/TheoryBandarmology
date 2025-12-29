import requests
import json
import sys
from .analyze_sentiment import analyze_sentiment

def define_params(type, symbol):
    if type == "forex":
        return f"FX:{symbol}"
    elif type == "commodity":
        return f"TV:{symbol}"
    else:
        return None
        

def fetch_tradingview_news(symbol):
    session = requests.Session()
    url = "https://news-mediator.tradingview.com/public/view/v1/symbol"
    
    params = [
        ('filter', 'lang:en'),
        ('filter', f'symbol:{symbol}'),
        ('client', 'web'),
        ('streaming', 'true'),
        ('user_prostatus', 'non_pro')
    ]

    headers = {
        "Accept": "text/event-stream",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Origin": "https://www.tradingview.com",
        "Referer": "https://www.tradingview.com/"
    }

    try:
        response = session.get(url, params=params, headers=headers, stream=True, timeout=60)
        
        if response.status_code != 200:
            print(f"Gagal koneksi. Status: {response.status_code}")
            return

        for line in response.iter_lines(decode_unicode=True):
            if line:
                if line.startswith("data:"):
                    raw_json = line[5:].strip()
                # 2. Menangani baris yang merupakan JSON langsung (Data awal/History)
                elif line.startswith("{"):
                    raw_json = line.strip()
                else:
                    continue

                try:
                    data = json.loads(raw_json)
                    
                    # Cek jika ada key 'items' dalam JSON
                    if "items" in data:
                        for item in data["items"]:
                            title = item.get("title")
                            published = item.get("published")
                            source = item.get("provider", {}).get("name", "TV")
                            
                            sentiment = analyze_sentiment(title)

                    # Jika hanya update streaming channel (bukan berita)
                    elif "streaming" in data:
                        print(f"--- Channel Stream Aktif: {data['streaming'].get('channel')} ---")

                except json.JSONDecodeError:
                    continue

    except requests.exceptions.ChunkedEncodingError:
        fetch_tradingview_news(symbol)
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")