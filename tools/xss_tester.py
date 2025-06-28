def test_xss(url):
    payload = "<script>alert(1)</script>"
    test_url = f"{url}?q={payload}"
    return f"Tested URL: {test_url} — Check in browser manually"