import requests

def check_headers(url):
    try:
        response = requests.get(url)
        return dict(response.headers)
    except Exception as e:
        return {"Error": str(e)}