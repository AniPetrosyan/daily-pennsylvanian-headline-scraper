import requests
from bs4 import BeautifulSoup

def scrape_latest_editorial():
    url = "https://www.thedp.com/section/editorials"
    response = requests.get(url)
    
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        return "BeautifulSoup is working fine."
    else:
        return f"Failed to retrieve the page, status code: {response.status_code}"

if __name__ == "__main__":
    result = scrape_latest_editorial()
    print(result)
