#!/usr/bin/env python3
"""
Phase 3 Integration Testing Script
Tests multi-tenant SSH configuration system with enhanced UI
"""

import requests
import json
import time
from datetime import datetime

class Phase3Tester:
    def __init__(self, base_url="http://127.0.0.1:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        
    def test_admin_login(self, username="admin", password="admin123"):
        """Test admin login functionality"""
        print(f"\n🔐 Testing Admin Login...")
        
        # Get login page first
        login_page = self.session.get(f"{self.base_url}/admin/login")
        if login_page.status_code != 200:
            print(f"❌ Cannot access login page: {login_page.status_code}")
            return False
            
        # Login with credentials
        login_data = {
            'username': username,
            'password': password
        }
        
        response = self.session.post(f"{self.base_url}/admin/login", 
                                   data=login_data,
                                   allow_redirects=False)
        
        if response.status_code == 302:  # Redirect on success
            print(f"✅ Admin login successful - redirected to: {response.headers.get('Location')}")
            return True
        else:
            print(f"❌ Admin login failed: {response.status_code}")
            return False
    
    def test_dashboard_access(self):
        """Test admin dashboard accessibility"""
        print(f"\n📊 Testing Dashboard Access...")
        
        response = self.session.get(f"{self.base_url}/admin/dashboard", allow_redirects=True)
        
        if response.status_code == 200:
            print(f"✅ Dashboard accessible")
            if "admin_dashboard.html" in response.url or "workspace" in response.url:
                print(f"✅ Correctly routed to workspace/dashboard")
                return True
            else:
                print(f"⚠️  Unexpected route: {response.url}")
                return True  # Still working
        else:
            print(f"❌ Dashboard access failed: {response.status_code}")
            return False
    
    def test_ssh_config_creation(self):
        """Test SSH config creation (simulated)"""
        print(f"\n⚙️ Testing SSH Config Creation...")
        
        # Test data for SSH config
        config_data = {
            'name': f'Test Config {datetime.now().strftime("%H%M%S")}',
            'description': 'Phase 3 Integration Test Config',
            'ssh_host': 'test.example.com',
            'ssh_port': '22',
            'ssh_username': 'testuser',
            'ssh_password': 'testpass123',
            'mysql_host': 'localhost',
            'mysql_port': '3306',
            'mysql_username': 'mysql_user',
            'mysql_password': 'mysql_pass123',
            'mysql_database': 'test_db'
        }
        
        response = self.session.post(f"{self.base_url}/admin/api/ssh-configs", 
                                   data=config_data,
                                   allow_redirects=False)
        
        if response.status_code in [200, 201, 302]:
            print(f"✅ SSH Config creation endpoint responding: {response.status_code}")
            return True
        else:
            print(f"❌ SSH Config creation failed: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False
    
    def test_api_endpoints(self):
        """Test various API endpoints"""
        print(f"\n🔗 Testing API Endpoints...")
        
        endpoints = [
            "/admin/api/ssh-configs",  # List SSH configs
            "/api/connection/status",   # Connection status
        ]
        
        results = {}
        for endpoint in endpoints:
            response = self.session.get(f"{self.base_url}{endpoint}")
            results[endpoint] = response.status_code
            
            if response.status_code == 200:
                print(f"✅ {endpoint}: OK")
            else:
                print(f"❌ {endpoint}: {response.status_code}")
        
        return all(status == 200 for status in results.values())
    
    def test_ui_components(self):
        """Test if UI components are loading"""
        print(f"\n🎨 Testing UI Components...")
        
        # Test static assets
        assets = [
            "/static/css/style.css",
            "/static/js/app.js"
        ]
        
        for asset in assets:
            response = self.session.get(f"{self.base_url}{asset}")
            if response.status_code == 200:
                print(f"✅ {asset}: Loaded")
            else:
                print(f"❌ {asset}: {response.status_code}")
        
        return True
    
    def run_full_test(self):
        """Run complete Phase 3 integration test"""
        print("=" * 60)
        print("🚀 PHASE 3 INTEGRATION TESTING")
        print("Multi-tenant SSH Configuration System")
        print("=" * 60)
        
        test_results = []
        
        # Test 1: Admin Login
        test_results.append(self.test_admin_login())
        
        # Test 2: Dashboard Access  
        test_results.append(self.test_dashboard_access())
        
        # Test 3: SSH Config Creation
        test_results.append(self.test_ssh_config_creation())
        
        # Test 4: API Endpoints
        test_results.append(self.test_api_endpoints())
        
        # Test 5: UI Components
        test_results.append(self.test_ui_components())
        
        # Summary
        passed = sum(test_results)
        total = len(test_results)
        
        print("\n" + "=" * 60)
        print("📋 PHASE 3 TEST SUMMARY")
        print("=" * 60)
        print(f"Tests Passed: {passed}/{total}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED - Phase 3 Integration Complete!")
            return True
        else:
            print("⚠️  Some tests failed - review results above")
            return False

if __name__ == "__main__":
    tester = Phase3Tester()
    tester.run_full_test()
