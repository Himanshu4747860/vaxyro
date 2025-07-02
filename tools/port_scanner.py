import socket

def scan_ports(target):
    open_ports = []
    for port in [21, 22, 23, 80, 443, 3306]:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((target, port))
            if result == 0:
                open_ports.append(f"Port {port} is open")
            sock.close()
        except:
            continue
    return open_ports or ["No open ports found."]