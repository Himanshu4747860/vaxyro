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

# You can continue copying other tools from your old code here...

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)