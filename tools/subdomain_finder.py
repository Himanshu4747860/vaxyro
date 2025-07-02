import requests

def find_subdomains(domain):
    try:
        url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
        response = requests.get(url)
        if response.ok:
            lines = response.text.splitlines()
            return [f"http://{line.split(',')[0]}" for line in lines if ',' in line]
        else:
            return ["Error: Unable to fetch data."]
    except Exception as e:
        return [str(e)]