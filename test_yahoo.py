import httpx
import re
from urllib.parse import unquote

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9'
}

for item in ["Horlicks jar", "Maggi 2-Minute Noodles", "Dettol Soap", "Fortune Sunflower Oil"]:
    url = f"https://images.search.yahoo.com/search/images?p={item.replace(' ', '+')}"
    r = httpx.get(url, headers=headers, follow_redirects=True, timeout=6.0)
    print("Item:", item, "Status:", r.status_code)
    # Yahoo encodes image URLs as imgurl=https%3A%2F%2F...
    raw_urls = re.findall(r'imgurl=(https?%3A%2F%2F[^&"\']+)', r.text)
    decoded = [unquote(u) for u in raw_urls if any(ext in unquote(u).lower() for ext in ['.jpg', '.jpeg', '.png'])]
    print("Found images:", len(decoded))
    for u in decoded[:3]:
        print("  ->", u)
