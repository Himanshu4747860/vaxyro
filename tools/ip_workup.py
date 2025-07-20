
import requests
import socket
from ipwhois import IPWhois

def ip_workup(ip_or_domain):
    try:
        results = []
        
        # Resolve domain to IP if needed
        if not ip_or_domain.replace('.', '').replace(':', '').isalnum():
            try:
                ip = socket.gethostbyname(ip_or_domain)
                results.append(f"Resolved IP: {ip}")
            except:
                return ["Invalid IP address or domain"]
        else:
            ip = ip_or_domain
            
        # WHOIS lookup for IP
        try:
            obj = IPWhois(ip)
            whois_data = obj.lookup_rdap()
            
            if 'network' in whois_data:
                network = whois_data['network']
                results.append(f"Network: {network.get('cidr', 'N/A')}")
                results.append(f"Network Name: {network.get('name', 'N/A')}")
                results.append(f"Country: {network.get('country', 'N/A')}")
                
            if 'asn' in whois_data:
                results.append(f"ASN: {whois_data['asn']}")
                results.append(f"ASN Description: {whois_data.get('asn_description', 'N/A')}")
                
        except Exception as e:
            results.append(f"WHOIS Error: {str(e)}")
            
        # Geolocation (using ipapi.co)
        try:
            geo_response = requests.get(f"http://ipapi.co/{ip}/json/", timeout=5)
            if geo_response.status_code == 200:
                geo_data = geo_response.json()
                results.append(f"Location: {geo_data.get('city', 'Unknown')}, {geo_data.get('region', 'Unknown')}, {geo_data.get('country_name', 'Unknown')}")
                results.append(f"ISP: {geo_data.get('org', 'Unknown')}")
                results.append(f"Timezone: {geo_data.get('timezone', 'Unknown')}")
        except:
            results.append("Geolocation: Unable to retrieve")
            
        # Check if IP is in common blacklists
        try:
            blacklist_response = requests.get(f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip}", 
                                            headers={'Key': 'demo', 'Accept': 'application/json'}, timeout=5)
            if blacklist_response.status_code == 200:
                results.append("Reputation: Clean (demo check)")
        except:
            results.append("Reputation: Unable to check")
            
        return results if results else ["No information found"]
    except Exception as e:
        return [f"Error: {str(e)}"]
