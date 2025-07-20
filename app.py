
from flask import Flask, render_template, request, jsonify
from tools.subdomain import run as run_subdomain
from tools.whois_lookup import whois_lookup
from tools.reverse_dns import reverse_dns_lookup
from tools.ip_workup import ip_workup
from tools.firewall_test import test_firewall
from tools.geo_ip import geo_ip_lookup
from tools.cms_detector import detect_cms
from tools.ai_vulnerability_scanner import ai_vulnerability_scan
import socket
import subprocess
import requests

app = Flask(__name__, static_folder="static", template_folder="templates")

# Tool categories for organization
TOOL_CATEGORIES = {
    'reconnaissance': {
        'name': 'Reconnaissance & Discovery',
        'description': 'Tools for gathering information about targets',
        'tools': ['subdomain', 'whois', 'reverse', 'portscan']
    },
    'network': {
        'name': 'Network Analysis',
        'description': 'Network security and analysis tools',
        'tools': ['portscan', 'firewall', 'geoip', 'ipworkup']
    },
    'web': {
        'name': 'Web Application Security',
        'description': 'Tools for analyzing web applications',
        'tools': ['xss', 'cms', 'headers', 'vulnscan']
    },
    'intelligence': {
        'name': 'Threat Intelligence',
        'description': 'Vulnerability and threat analysis tools',
        'tools': ['cve', 'vulnscan', 'geoip']
    }
}

# Tool metadata for search and display
TOOLS_METADATA = {
    'subdomain': {
        'name': 'Subdomain Finder',
        'description': 'Discover hidden subdomains and map attack surfaces using advanced enumeration techniques',
        'keywords': ['subdomain', 'discovery', 'enumeration', 'reconnaissance', 'dns'],
        'icon': '🔍',
        'gradient': 'from-green-400 to-blue-500'
    },
    'portscan': {
        'name': 'Port Scanner',
        'description': 'Identify open ports and running services with fast multi-threaded scanning',
        'keywords': ['port', 'scan', 'service', 'network', 'tcp', 'udp'],
        'icon': '🔌',
        'gradient': 'from-blue-400 to-purple-500'
    },
    'xss': {
        'name': 'XSS Tester',
        'description': 'Test for cross-site scripting vulnerabilities with advanced payload detection',
        'keywords': ['xss', 'cross-site', 'scripting', 'injection', 'web', 'vulnerability'],
        'icon': '⚡',
        'gradient': 'from-purple-400 to-pink-500'
    },
    'cve': {
        'name': 'CVE Lookup',
        'description': 'Search for known security vulnerabilities and exploits in CVE database',
        'keywords': ['cve', 'vulnerability', 'exploit', 'security', 'database'],
        'icon': '🛡️',
        'gradient': 'from-yellow-400 to-red-500'
    },
    'headers': {
        'name': 'Header Analyzer',
        'description': 'Analyze HTTP headers for security issues and misconfigurations',
        'keywords': ['header', 'http', 'security', 'analysis', 'web'],
        'icon': '📊',
        'gradient': 'from-teal-400 to-indigo-500'
    },
    'whois': {
        'name': 'WHOIS Lookup',
        'description': 'Get comprehensive domain registration and ownership information',
        'keywords': ['whois', 'domain', 'registration', 'ownership', 'dns'],
        'icon': '📋',
        'gradient': 'from-indigo-400 to-cyan-500'
    },
    'reverse': {
        'name': 'Reverse DNS',
        'description': 'Perform reverse DNS lookups and comprehensive DNS record analysis',
        'keywords': ['reverse', 'dns', 'lookup', 'hostname', 'ip'],
        'icon': '🔄',
        'gradient': 'from-cyan-400 to-green-500'
    },
    'ipworkup': {
        'name': 'IP Intelligence',
        'description': 'Comprehensive IP address analysis including WHOIS, ASN, and reputation data',
        'keywords': ['ip', 'analysis', 'whois', 'asn', 'reputation'],
        'icon': '🌐',
        'gradient': 'from-orange-400 to-red-500'
    },
    'firewall': {
        'name': 'Firewall Tester',
        'description': 'Advanced firewall detection and bypass testing with stealth techniques',
        'keywords': ['firewall', 'security', 'testing', 'bypass', 'network'],
        'icon': '🔥',
        'gradient': 'from-red-400 to-orange-500'
    },
    'geoip': {
        'name': 'Geo IP Tracker',
        'description': 'Track geographical location and ISP information for IP addresses',
        'keywords': ['geo', 'ip', 'location', 'tracking', 'geographical'],
        'icon': '🌍',
        'gradient': 'from-emerald-400 to-teal-500'
    },
    'cms': {
        'name': 'CMS Detector',
        'description': 'Identify content management systems and web technologies with high accuracy',
        'keywords': ['cms', 'content', 'management', 'detection', 'web', 'technology'],
        'icon': '🎯',
        'gradient': 'from-violet-400 to-purple-500'
    },
    'vulnscan': {
        'name': 'AI Vulnerability Scanner',
        'description': 'AI-powered comprehensive vulnerability assessment and security analysis',
        'keywords': ['vulnerability', 'scanner', 'ai', 'security', 'assessment'],
        'icon': '🤖',
        'gradient': 'from-pink-400 to-rose-500'
    }
}

@app.route('/')
def index():
    return render_template('index.html', tools_metadata=TOOLS_METADATA, categories=TOOL_CATEGORIES)

@app.route('/api/search')
def search_tools():
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify([])
    
    results = []
    for tool_id, metadata in TOOLS_METADATA.items():
        # Search in name, description, and keywords
        searchable_text = (
            metadata['name'] + ' ' +
            metadata['description'] + ' ' +
            ' '.join(metadata['keywords'])
        ).lower()
        
        if query in searchable_text:
            score = 0
            # Higher score for name matches
            if query in metadata['name'].lower():
                score += 10
            # Medium score for keyword matches
            for keyword in metadata['keywords']:
                if query in keyword:
                    score += 5
            # Lower score for description matches
            if query in metadata['description'].lower():
                score += 1
                
            results.append({
                'id': tool_id,
                'name': metadata['name'],
                'description': metadata['description'],
                'icon': metadata['icon'],
                'score': score
            })
    
    # Sort by relevance score
    results.sort(key=lambda x: x['score'], reverse=True)
    return jsonify(results[:6])  # Return top 6 results

@app.route('/subdomain', methods=['GET', 'POST'])
def subdomain_tool():
    if request.method == 'POST':
        target = request.form.get('target')
        try:
            result = run_subdomain(target)
            return render_template('tool_result.html', tool="Subdomain Finder", target=target, result=result)
        except Exception as e:
            return render_template('tool_result.html', tool="Subdomain Finder", target=target, result=[f"Error: {str(e)}"])
    return render_template('tool_form.html', title="Subdomain Finder", description=TOOLS_METADATA['subdomain']['description'])

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
    return render_template('tool_form.html', title="Port Scanner", description=TOOLS_METADATA['portscan']['description'])

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
    return render_template('tool_form.html', title="XSS Tester", description=TOOLS_METADATA['xss']['description'])

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
    return render_template('tool_form.html', title="CVE Lookup", description=TOOLS_METADATA['cve']['description'])

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
    return render_template('tool_form.html', title="Header Analyzer", description=TOOLS_METADATA['headers']['description'])

@app.route('/whois', methods=['GET', 'POST'])
def whois_tool():
    if request.method == 'POST':
        target = request.form.get('target')
        try:
            result = whois_lookup(target)
            return render_template('tool_result.html', tool="WHOIS Lookup", target=target, result=result)
        except Exception as e:
            return render_template('tool_result.html', tool="WHOIS Lookup", target=target, result=[f"Error: {str(e)}"])
    return render_template('tool_form.html', title="WHOIS Lookup", description=TOOLS_METADATA['whois']['description'])

@app.route('/reverse', methods=['GET', 'POST'])
def reverse_tool():
    if request.method == 'POST':
        target = request.form.get('target')
        try:
            result = reverse_dns_lookup(target)
            return render_template('tool_result.html', tool="Reverse DNS", target=target, result=result)
        except Exception as e:
            return render_template('tool_result.html', tool="Reverse DNS", target=target, result=[f"Error: {str(e)}"])
    return render_template('tool_form.html', title="Reverse DNS", description=TOOLS_METADATA['reverse']['description'])

@app.route('/ipworkup', methods=['GET', 'POST'])
def ipworkup_tool():
    if request.method == 'POST':
        target = request.form.get('target')
        try:
            result = ip_workup(target)
            return render_template('tool_result.html', tool="IP Intelligence", target=target, result=result)
        except Exception as e:
            return render_template('tool_result.html', tool="IP Intelligence", target=target, result=[f"Error: {str(e)}"])
    return render_template('tool_form.html', title="IP Intelligence", description=TOOLS_METADATA['ipworkup']['description'])

@app.route('/firewall', methods=['GET', 'POST'])
def firewall_tool():
    if request.method == 'POST':
        target = request.form.get('target')
        try:
            result = test_firewall(target)
            return render_template('tool_result.html', tool="Firewall Tester", target=target, result=result)
        except Exception as e:
            return render_template('tool_result.html', tool="Firewall Tester", target=target, result=[f"Error: {str(e)}"])
    return render_template('tool_form.html', title="Firewall Tester", description=TOOLS_METADATA['firewall']['description'])

@app.route('/geoip', methods=['GET', 'POST'])
def geoip_tool():
    if request.method == 'POST':
        target = request.form.get('target')
        try:
            result = geo_ip_lookup(target)
            return render_template('tool_result.html', tool="Geo IP Tracker", target=target, result=result)
        except Exception as e:
            return render_template('tool_result.html', tool="Geo IP Tracker", target=target, result=[f"Error: {str(e)}"])
    return render_template('tool_form.html', title="Geo IP Tracker", description=TOOLS_METADATA['geoip']['description'])

@app.route('/cms', methods=['GET', 'POST'])
def cms_tool():
    if request.method == 'POST':
        target = request.form.get('target')
        try:
            result = detect_cms(target)
            return render_template('tool_result.html', tool="CMS Detector", target=target, result=result)
        except Exception as e:
            return render_template('tool_result.html', tool="CMS Detector", target=target, result=[f"Error: {str(e)}"])
    return render_template('tool_form.html', title="CMS Detector", description=TOOLS_METADATA['cms']['description'])

@app.route('/vulnscan', methods=['GET', 'POST'])
def vulnscan_tool():
    if request.method == 'POST':
        target = request.form.get('target')
        try:
            result = ai_vulnerability_scan(target)
            return render_template('tool_result.html', tool="AI Vulnerability Scanner", target=target, result=result)
        except Exception as e:
            return render_template('tool_result.html', tool="AI Vulnerability Scanner", target=target, result=[f"Error: {str(e)}"])
    return render_template('tool_form.html', title="AI Vulnerability Scanner", description=TOOLS_METADATA['vulnscan']['description'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
