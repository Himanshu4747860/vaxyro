import requests
from bs4 import BeautifulSoup

def search_cve(keyword):
    try:
        url = f"https://www.cvedetails.com/google-search-results.php?q={keyword}"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        results = soup.find_all('a', href=True)
        links = [a['href'] for a in results if "cve" in a['href'].lower()]
        return links[:5]
    except Exception as e:
        return [f"Error: {str(e)}"]