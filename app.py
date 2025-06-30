from flask import Flask, render_template, request, jsonify
import socket
import requests
import subprocess

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route('/')
def index():
    return render_template('index.html')

# ---------- Subdomain Finder ----------
@app.route('/subdomain', methods=['GET', 'POST'])
def subdomain_tool():
    if request.method == 'POST':
        target = request.form.get('target')
        subdomains = [f"mail.{target}", f"admin.{target}", f"dev.{target}"]
        return render_template('tool_result.html', tool="Subdomain Finder", target=target, result=subdomains)
    return render_template('tool_form.html', title="Subdomain Finder")

# ---------- Port Scanner ----------
@app.route('/portscan', methods=['GET', 'POST'])
def portscan():
    if request.method == 'POST':
        target = request.form.get('target')
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
        return render_template('tool_result.html', tool="Port Scanner", target=target, result=open_ports)
    return render_template('tool_form.html', title="Port Scanner")

# ---------- XSS Tester ----------
@app.route('/xss', methods=['GET', 'POST'])
def xss_tester():
    if request.method == 'POST':
        url = request.form.get('target')
        payload = "<script>alert('XSS')</script>"
        test_url = url + payload
        result = [f"Tested URL: {test_url}", "(Simulated test, not real XSS check)"]
        return render_template('tool_result.html', tool="XSS Tester", target=url, result=result)
    return render_template('tool_form.html', title="XSS Tester")

# ---------- CVE Lookup ----------
@app.route('/cve', methods=['GET', 'POST'])
def cve_lookup():
    if request.method == 'POST':
        keyword = request.form.get('target')
        result = [
            f"CVE-2023-1234 - Sample vulnerability in {keyword}",
            f"CVE-2022-5678 - Example issue with {keyword}"
        ]
        return render_template('tool_result.html', tool="CVE Lookup", target=keyword, result=result)
    return render_template('tool_form.html', title="CVE Lookup")

# ---------- HTTP Header Analyzer ----------
@app.route('/headers', methods=['GET', 'POST'])
def headers_tool():
    if request.method == 'POST':
        target = request.form.get('target')
        try:
            r = requests.get(target, timeout=3)
            result = [f"{key}: {value}" for key, value in r.headers.items()]
        except Exception as e:
            result = ["Error fetching headers", str(e)]
        return render_template('tool_result.html', tool="Header Analyzer", target=target, result=result)
    return render_template('tool_form.html', title="Header Analyzer")

# ---------- VX-Console UI ----------
@app.route('/console')
def console():
    return render_template('console.html')

# ---------- VX-Console Command Runner ----------
@app.route('/run', methods=['POST'])
def run_command():
    command = request.json.get('command')
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=5)
        return jsonify({"output": result.stdout + result.stderr})
    except Exception as e:
        return jsonify({"output": str(e)})

# ---------- Run App ----------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)