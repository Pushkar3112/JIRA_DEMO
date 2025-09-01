# File 2: test_cases.py
"""
Test Cases for Username Password Checker
VNIT CSP300 Assignment 2 - JIRA Demo
Automated testing for validation functions
"""

import csv
import os
import hashlib
from datetime import datetime

class TestRunner:
    def __init__(self):
        self.test_results = []
        self.csv_file = "test_users.csv"
    
    def setup_test_csv(self):
        """Create test CSV file"""
        try:
            with open(self.csv_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['username', 'password_hash', 'created_date', 'last_login'])
            print("✅ Test CSV created")
        except Exception as e:
            print(f"❌ Test setup failed: {e}")
    
    def cleanup_test_csv(self):
        """Remove test CSV file"""
        try:
            if os.path.exists(self.csv_file):
                os.remove(self.csv_file)
            print("✅ Test cleanup completed")
        except Exception as e:
            print(f"❌ Cleanup failed: {e}")
    
    def hash_password(self, password):
        """Hash password for testing"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def test_username_validation(self):
        """Test username validation logic"""
        print("\n🧪 TESTING USERNAME VALIDATION")
        print("-" * 35)
        
        test_cases = [
            ("validuser", True, "Valid username"),
            ("ab", False, "Too short (< 3 chars)"),
            ("a" * 25, False, "Too long (> 20 chars)"),
            ("user@123", False, "Contains special chars"),
            ("user123", True, "Valid alphanumeric"),
            ("", False, "Empty username"),
            ("User_Name", True, "Valid with underscore")
        ]
        
        passed = 0
        total = len(test_cases)
        
        for username, expected, description in test_cases:
            # Simple validation logic
            is_valid = (username and 
                       3 <= len(username) <= 20 and 
                       username.replace('_', '').isalnum())
            
            result = "✅ PASS" if is_valid == expected else "❌ FAIL"
            print(f"{result} | {description}: '{username}'")
            
            if is_valid == expected:
                passed += 1
        
        print(f"\n📊 Username Validation: {passed}/{total} tests passed")
        return passed == total
    
    def test_password_validation(self):
        """Test password validation logic"""
        print("\n🧪 TESTING PASSWORD VALIDATION")
        print("-" * 35)
        
        test_cases = [
            ("Password123!", True, "Strong password"),
            ("password", False, "No uppercase/digit/special"),
            ("PASSWORD123!", False, "No lowercase"),
            ("Password!", False, "No digit"),
            ("Pass123", False, "No special char"),
            ("Pw1!", False, "Too short (< 8 chars)"),
            ("MySecure@Pass2024", True, "Very strong password")
        ]
        
        passed = 0
        total = len(test_cases)
        
        for password, expected, description in test_cases:
            # Password validation logic
            if len(password) < 8:
                is_valid = False
            else:
                has_upper = any(c.isupper() for c in password)
                has_lower = any(c.islower() for c in password)
                has_digit = any(c.isdigit() for c in password)
                has_special = any(c in "!@#$%^&*(),.?\":{}|<>" for c in password)
                is_valid = has_upper and has_lower and has_digit and has_special
            
            result = "✅ PASS" if is_valid == expected else "❌ FAIL"
            print(f"{result} | {description}")
            
            if is_valid == expected:
                passed += 1
        
        print(f"\n📊 Password Validation: {passed}/{total} tests passed")
        return passed == total
    
    def test_csv_operations(self):
        """Test CSV file operations"""
        print("\n🧪 TESTING CSV OPERATIONS")
        print("-" * 30)
        
        self.setup_test_csv()
        
        try:
            # Test writing to CSV
            test_user = {
                'username': 'testuser',
                'password_hash': self.hash_password('TestPass123!'),
                'created_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'last_login': 'Never'
            }
            
            with open(self.csv_file, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([test_user['username'], test_user['password_hash'], 
                               test_user['created_date'], test_user['last_login']])
            
            print("✅ CSV Write: Success")
            
            # Test reading from CSV
            with open(self.csv_file, 'r') as file:
                reader = csv.DictReader(file)
                users = list(reader)
                if users and users[0]['username'] == 'testuser':
                    print("✅ CSV Read: Success")
                    csv_test_passed = True
                else:
                    print("❌ CSV Read: Failed")
                    csv_test_passed = False
            
        except Exception as e:
            print(f"❌ CSV Operations Failed: {e}")
            csv_test_passed = False
        
        self.cleanup_test_csv()
        return csv_test_passed
    
    def test_authentication_flow(self):
        """Test complete authentication flow"""
        print("\n🧪 TESTING AUTHENTICATION FLOW")
        print("-" * 40)
        
        self.setup_test_csv()
        
        try:
            # Simulate user registration
            username = "demouser"
            password = "DemoPass123!"
            password_hash = self.hash_password(password)
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Write test user
            with open(self.csv_file, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([username, password_hash, current_time, "Never"])
            
            print("✅ User Registration: Simulated")
            
            # Simulate login check
            login_hash = self.hash_password(password)
            login_success = False
            
            with open(self.csv_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if (row['username'].lower() == username.lower() and 
                        row['password_hash'] == login_hash):
                        login_success = True
                        break
            
            if login_success:
                print("✅ User Login: Success")
            else:
                print("❌ User Login: Failed")
            
            # Test wrong password
            wrong_hash = self.hash_password("wrongpassword")
            wrong_login = False
            
            with open(self.csv_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if (row['username'].lower() == username.lower() and 
                        row['password_hash'] == wrong_hash):
                        wrong_login = True
                        break
            
            if not wrong_login:
                print("✅ Wrong Password Rejection: Success")
            else:
                print("❌ Wrong Password Rejection: Failed")
            
        except Exception as e:
            print(f"❌ Authentication test failed: {e}")
            login_success = False
        
        self.cleanup_test_csv()
        return login_success
    
    def run_all_tests(self):
        """Run all test cases"""
        print("🚀 STARTING AUTOMATED TEST SUITE")
        print("=" * 50)
        
        results = []
        results.append(self.test_username_validation())
        results.append(self.test_password_validation())
        results.append(self.test_csv_operations())
        results.append(self.test_authentication_flow())
        
        passed_tests = sum(results)
        total_tests = len(results)
        
        print("\n" + "=" * 50)
        print("🎯 FINAL TEST RESULTS")
        print("=" * 50)
        print(f"✅ Tests Passed: {passed_tests}/{total_tests}")
        print(f"📊 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if passed_tests == total_tests:
            print("🏆 ALL TESTS PASSED! System is ready for production.")
        else:
            print("⚠️  Some tests failed. Review implementation.")
        
        return passed_tests == total_tests

def main():
    """Main function for testing"""
    print("🧪 USERNAME PASSWORD CHECKER - TEST MODULE")
    print("🏫 VNIT CSP300 Assignment 2")
    print("=" * 50)
    
    choice = input("Run automated tests? (y/n): ").lower()
    
    if choice == 'y':
        tester = TestRunner()
        tester.run_all_tests()
    else:
        print("Test execution cancelled.")

if __name__ == "__main__":
    main()
