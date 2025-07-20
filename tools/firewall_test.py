
import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor

def test_firewall(target):
    try:
        results = []
        
        # Common ports to test
        common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 1433, 3306, 3389, 5432, 8080, 8443]
        
        # High ports to test
        high_ports = [8000, 8001, 8008, 8080, 8443, 8888, 9000, 9001, 9090, 10000]
        
        all_ports = common_ports + high_ports
        
        results.append(f"Testing {len(all_ports)} ports on {target}")
        results.append("=" * 50)
        
        open_ports = []
        filtered_ports = []
        closed_ports = []
        
        def scan_port(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target, port))
                
                if result == 0:
                    # Port is open
                    try:
                        service = socket.getservbyport(port)
                    except:
                        service = "unknown"
                    open_ports.append(f"Port {port}/tcp OPEN ({service})")
                else:
                    closed_ports.append(port)
                    
                sock.close()
            except socket.timeout:
                filtered_ports.append(f"Port {port}/tcp FILTERED (timeout)")
            except Exception:
                closed_ports.append(port)
        
        # Use threading for faster scanning
        with ThreadPoolExecutor(max_workers=50) as executor:
            executor.map(scan_port, all_ports)
        
        # Add results
        if open_ports:
            results.append("OPEN PORTS:")
            results.extend(open_ports)
            results.append("")
            
        if filtered_ports:
            results.append("FILTERED PORTS:")
            results.extend(filtered_ports[:10])  # Limit output
            if len(filtered_ports) > 10:
                results.append(f"... and {len(filtered_ports) - 10} more filtered ports")
            results.append("")
            
        results.append(f"SUMMARY: {len(open_ports)} open, {len(filtered_ports)} filtered, {len(closed_ports)} closed")
        
        # Firewall detection heuristics
        if len(filtered_ports) > len(open_ports) * 2:
            results.append("ANALYSIS: Strong firewall detected (many filtered ports)")
        elif len(open_ports) == 0:
            results.append("ANALYSIS: Host appears to be behind strict firewall or offline")
        elif len(open_ports) > 10:
            results.append("ANALYSIS: Multiple services exposed - review security posture")
        else:
            results.append("ANALYSIS: Standard firewall configuration detected")
            
        return results
    except Exception as e:
        return [f"Error: {str(e)}"]
