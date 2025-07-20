
import requests
import json

def geo_ip_lookup(ip_or_domain):
    try:
        results = []
        
        # Resolve domain to IP if needed
        if not ip_or_domain.replace('.', '').replace(':', '').isalnum():
            import socket
            try:
                ip = socket.gethostbyname(ip_or_domain)
                results.append(f"Resolved {ip_or_domain} to {ip}")
            except:
                return ["Invalid IP address or domain"]
        else:
            ip = ip_or_domain
            
        # Multiple geolocation services for accuracy
        services = [
            {
                'name': 'IPInfo',
                'url': f'http://ipinfo.io/{ip}/json',
                'fields': ['city', 'region', 'country', 'loc', 'org', 'timezone']
            },
            {
                'name': 'IP-API',
                'url': f'http://ip-api.com/json/{ip}',
                'fields': ['city', 'regionName', 'country', 'lat', 'lon', 'isp', 'timezone']
            }
        ]
        
        for service in services:
            try:
                response = requests.get(service['url'], timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    results.append(f"\n--- {service['name']} Data ---")
                    
                    if service['name'] == 'IPInfo':
                        results.append(f"City: {data.get('city', 'Unknown')}")
                        results.append(f"Region: {data.get('region', 'Unknown')}")
                        results.append(f"Country: {data.get('country', 'Unknown')}")
                        if 'loc' in data:
                            coords = data['loc'].split(',')
                            results.append(f"Coordinates: {coords[0]}, {coords[1]}")
                        results.append(f"ISP/Org: {data.get('org', 'Unknown')}")
                        results.append(f"Timezone: {data.get('timezone', 'Unknown')}")
                        
                    elif service['name'] == 'IP-API':
                        results.append(f"City: {data.get('city', 'Unknown')}")
                        results.append(f"Region: {data.get('regionName', 'Unknown')}")
                        results.append(f"Country: {data.get('country', 'Unknown')}")
                        results.append(f"Coordinates: {data.get('lat', 'Unknown')}, {data.get('lon', 'Unknown')}")
                        results.append(f"ISP: {data.get('isp', 'Unknown')}")
                        results.append(f"Timezone: {data.get('timezone', 'Unknown')}")
                        
                    break  # Use first successful service
            except Exception as e:
                continue
                
        # Additional security checks
        try:
            # Check if it's a VPN/Proxy (simplified check)
            vpn_response = requests.get(f"http://ip-api.com/json/{ip}?fields=proxy", timeout=5)
            if vpn_response.status_code == 200:
                vpn_data = vpn_response.json()
                if vpn_data.get('proxy'):
                    results.append("\n--- Security Analysis ---")
                    results.append("⚠️  VPN/Proxy detected")
        except:
            pass
            
        return results if results else ["No geographical data found"]
    except Exception as e:
        return [f"Error: {str(e)}"]
