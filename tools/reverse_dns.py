
import socket
import dns.resolver
import dns.reversename

def reverse_dns_lookup(ip_or_domain):
    try:
        results = []
        
        # If it's a domain, get IP first
        if not ip_or_domain.replace('.', '').isdigit():
            try:
                ip = socket.gethostbyname(ip_or_domain)
                results.append(f"Forward DNS: {ip_or_domain} → {ip}")
            except:
                return ["Invalid domain or IP address"]
        else:
            ip = ip_or_domain
            
        # Reverse DNS lookup
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            results.append(f"Reverse DNS: {ip} → {hostname}")
        except:
            results.append(f"No reverse DNS record found for {ip}")
            
        # Additional DNS records
        try:
            if not ip_or_domain.replace('.', '').isdigit():
                domain = ip_or_domain
                for record_type in ['A', 'AAAA', 'MX', 'TXT', 'NS', 'CNAME']:
                    try:
                        answers = dns.resolver.resolve(domain, record_type)
                        for answer in answers:
                            results.append(f"{record_type} Record: {answer}")
                    except:
                        continue
        except:
            pass
            
        return results if results else ["No DNS information found"]
    except Exception as e:
        return [f"Error: {str(e)}"]
