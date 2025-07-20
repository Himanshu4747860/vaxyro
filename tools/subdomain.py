# tools/subdomain.py
import requests

def run(target):
    res = requests.get(f"https://api.hackertarget.com/hostsearch/?q={target}")
    if res.status_code == 200:
        lines = res.text.strip().split('\n')
        subdomains = [line.split(',')[0] for line in lines if line]
        return subdomains
    else:
        return ["API request failed."]