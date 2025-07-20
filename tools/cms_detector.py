
import requests
from bs4 import BeautifulSoup
import re

def detect_cms(url):
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
            
        results = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        content = response.text.lower()
        
        # CMS Detection patterns
        cms_patterns = {
            'WordPress': [
                r'wp-content',
                r'wp-includes',
                r'wp-admin',
                r'wordpress',
                r'wp-json'
            ],
            'Joomla': [
                r'/joomla/',
                r'joomla',
                r'/administrator/',
                r'com_content',
                r'option=com_'
            ],
            'Drupal': [
                r'drupal',
                r'/sites/default/',
                r'/sites/all/',
                r'drupal.org',
                r'/node/'
            ],
            'Magento': [
                r'magento',
                r'/skin/frontend/',
                r'/js/mage/',
                r'mage/cookies',
                r'/customer/account/'
            ],
            'Shopify': [
                r'shopify',
                r'cdn.shopify.com',
                r'/checkout',
                r'shopify_pay'
            ],
            'Django': [
                r'django',
                r'csrfmiddlewaretoken',
                r'/admin/login/'
            ],
            'Laravel': [
                r'laravel',
                r'laravel_session',
                r'/storage/framework/'
            ]
        }
        
        detected_cms = []
        
        # Check content for CMS patterns
        for cms, patterns in cms_patterns.items():
            matches = 0
            for pattern in patterns:
                if re.search(pattern, content):
                    matches += 1
            if matches >= 1:
                confidence = min(100, (matches / len(patterns)) * 100)
                detected_cms.append(f"{cms} (Confidence: {confidence:.0f}%)")
        
        # Check HTTP headers
        server_header = response.headers.get('Server', '').lower()
        x_powered_by = response.headers.get('X-Powered-By', '').lower()
        
        if 'apache' in server_header:
            results.append(f"Web Server: Apache")
        elif 'nginx' in server_header:
            results.append(f"Web Server: Nginx")
        elif 'iis' in server_header:
            results.append(f"Web Server: IIS")
            
        if x_powered_by:
            results.append(f"Powered By: {x_powered_by}")
        
        # Check for meta generators
        soup = BeautifulSoup(response.text, 'html.parser')
        generator_meta = soup.find('meta', attrs={'name': 'generator'})
        if generator_meta:
            results.append(f"Generator: {generator_meta.get('content', 'Unknown')}")
        
        # Add detected CMS
        if detected_cms:
            results.append("\n--- CMS Detection ---")
            results.extend(detected_cms)
        else:
            results.append("No CMS detected or custom framework")
            
        # Check for common frameworks/libraries
        frameworks = {
            'React': r'react',
            'Vue.js': r'vue\.js',
            'Angular': r'angular',
            'jQuery': r'jquery',
            'Bootstrap': r'bootstrap'
        }
        
        detected_frameworks = []
        for framework, pattern in frameworks.items():
            if re.search(pattern, content):
                detected_frameworks.append(framework)
                
        if detected_frameworks:
            results.append("\n--- Frontend Frameworks ---")
            results.extend(detected_frameworks)
            
        return results if results else ["Unable to detect CMS or framework"]
    except Exception as e:
        return [f"Error: {str(e)}"]
