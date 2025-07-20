from flask import Flask, render_template, request, jsonify
from tools.subdomain import run as run_subdomain
import socket
import subprocess
import requests

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/subdomain', methods=['GET', 'POST'])
def subdomain_tool():
    if request.method == 'POST':
        target = request.form.get('target')
        try:
            result = run_subdomain(target)
            return render_template('tool_result.html', tool="Subdomain Finder", target=target, result=result)
        except Exception as e:
            return render_template('tool_result.html', tool="Subdomain Finder", target=target, result=[f"Error: {str(e)}"])
    return render_template('tool_form.html', title="Subdomain Finder")

@app.route('/portscan', methods=['GET', 'POST'])
def portscan_tool():
    if request.method == 'POST':
        target = request.form.get('target')
        try:
            from tools.port_scanner import scan_ports
            result = scan_ports(target)
            return render_template('tool_result.html', tool="Port Scanner", target=target, result=result)
        except Exception as e:
            return render_template('tool_result.html', tool="Port Scanner", target=target, result=[f"Error: {str(e)}"])
    return render_template('tool_form.html', title="Port Scanner")

@app.route('/xss', methods=['GET', 'POST'])
def xss_tool():
    if request.method == 'POST':
        target = request.form.get('target')
        try:
            from tools.xss_tester import test_xss
            result = test_xss(target)
            return render_template('tool_result.html', tool="XSS Tester", target=target, result=[result])
        except Exception as e:
            return render_template('tool_result.html', tool="XSS Tester", target=target, result=[f"Error: {str(e)}"])
    return render_template('tool_form.html', title="XSS Tester")

@app.route('/cve', methods=['GET', 'POST'])
def cve_tool():
    if request.method == 'POST':
        target = request.form.get('target')
        try:
            from tools.cve_checker import search_cve
            result = search_cve(target)
            return render_template('tool_result.html', tool="CVE Lookup", target=target, result=result)
        except Exception as e:
            return render_template('tool_result.html', tool="CVE Lookup", target=target, result=[f"Error: {str(e)}"])
    return render_template('tool_form.html', title="CVE Lookup")

@app.route('/headers', methods=['GET', 'POST'])
def headers_tool():
    if request.method == 'POST':
        target = request.form.get('target')
        try:
            from tools.header_checker import check_headers
            result = check_headers(target)
            formatted_result = [f"{k}: {v}" for k, v in result.items()]
            return render_template('tool_result.html', tool="Header Analyzer", target=target, result=formatted_result)
        except Exception as e:
            return render_template('tool_result.html', tool="Header Analyzer", target=target, result=[f"Error: {str(e)}"])
    return render_template('tool_form.html', title="Header Analyzer")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)