import socket

def run_port_scanner(host):
    open_ports = []
    common_ports = [21, 22, 23, 25, 53, 80, 110, 443, 8080]
    for port in common_ports:
        try:
            sock = socket.socket()
            sock.settimeout(0.5)
            result = sock.connect_ex((host, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
        except:
            pass
    return open_ports