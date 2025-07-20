
import whois
from datetime import datetime

def whois_lookup(domain):
    try:
        w = whois.whois(domain)
        result = []
        
        if w.domain_name:
            result.append(f"Domain Name: {w.domain_name[0] if isinstance(w.domain_name, list) else w.domain_name}")
        if w.registrar:
            result.append(f"Registrar: {w.registrar}")
        if w.creation_date:
            date = w.creation_date[0] if isinstance(w.creation_date, list) else w.creation_date
            result.append(f"Creation Date: {date}")
        if w.expiration_date:
            date = w.expiration_date[0] if isinstance(w.expiration_date, list) else w.expiration_date
            result.append(f"Expiration Date: {date}")
        if w.name_servers:
            ns = ', '.join(w.name_servers) if isinstance(w.name_servers, list) else w.name_servers
            result.append(f"Name Servers: {ns}")
        if w.status:
            status = ', '.join(w.status) if isinstance(w.status, list) else w.status
            result.append(f"Status: {status}")
        if w.org:
            result.append(f"Organization: {w.org}")
        if w.country:
            result.append(f"Country: {w.country}")
            
        return result if result else ["No WHOIS data found"]
    except Exception as e:
        return [f"Error: {str(e)}"]
