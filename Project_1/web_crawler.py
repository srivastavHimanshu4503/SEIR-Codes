import requests

class WebCrawlerClient:
    def __init__(self, url): 
        self.url = url

    def fetch(self):
        try:
            result = requests.get(self.url, timeout=10, headers={
                    "User-Agent":
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
                }
            )

            result.raise_for_status()
            return result.text
        
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to fetch {self.url}: {e}")