# File 1: main.py
"""
Username Password Checker Syste
VNIT CSP300 Assignment 2 - JIRA Dem
Simple 2-file implementation
"""

import csv
import hashlib
import os
import getpass
from datetime import datetime

class AuthSystem:
    def __init__(self):
        self.csv_file = "users.csv"
        self.init_csv()
    
    def init_csv(self):
        """Initialize CSV file if it doesn't exist"""
        try:
            if not os.path.exists(self.csv_file):
                with open(self.csv_file, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['username', 'password_hash', 'created_date', 'last_login'])
                print(f"✅ Created CSV file: {self.csv_file}")
        except Exception as e:
            print(f"❌ CSV Error: {e}")
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def validate_username(self, username):
        """Validate username (3-20 chars, alphanumeric)"""
        if not username or len(username) < 3 or len(username) > 20:
            return False
        return username.isalnum()
    
    def validate_password(self, password):
        """Validate password strength"""
        if len(password) < 8:
            return False
        
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*(),.?\":{}|<>" for c in password)
        
        return has_upper and has_lower and has_digit and has_special
    
    def username_exists(self, username):
        """Check if username already exists"""
        try:
            with open(self.csv_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['username'].lower() == username.lower():
                        return True
            return False
        except FileNotFoundError:
            return False
        except Exception as e:
            print(f"❌ Error checking username: {e}")
            return False
    
    def register_user(self):
        """Register new user"""
        try:
            print("\n🔐 USER REGISTRATION")
            print("-" * 25)
            
            # Get username
            while True:
                username = input("Enter username (3-20 chars): ").strip()
                if not self.validate_username(username):
                    print("❌ Invalid username! Use 3-20 alphanumeric characters.")
                    continue
                if self.username_exists(username):
                    print("❌ Username already exists! Try another.")
                    continue
                break
            
            # Get password
            while True:
                password = getpass.getpass("Enter password (8+ chars, mixed case, digit, special): ")
                if not self.validate_password(password):
                    print("❌ Weak password! Need 8+ chars with uppercase, lowercase, digit, special char.")
                    continue
                
                confirm = getpass.getpass("Confirm password: ")
                if password != confirm:
                    print("❌ Passwords don't match!")
                    continue
                break
            
            # Save user
            password_hash = self.hash_password(password)
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            with open(self.csv_file, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([username, password_hash, current_time, "Never"])
            
            print(f"✅ User '{username}' registered successfully!")
            
        except Exception as e:
            print(f"❌ Registration failed: {e}")
    
    def login_user(self):
        """Login existing user"""
        try:
            print("\n🔑 USER LOGIN")
            print("-" * 15)
            
            username = input("Username: ").strip()
            password = getpass.getpass("Password: ")
            
            if not os.path.exists(self.csv_file):
                print("❌ No users registered yet!")
                return
            
            password_hash = self.hash_password(password)
            
            # Read and check users
            users = []
            user_found = False
            login_success = False
            
            with open(self.csv_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['username'].lower() == username.lower():
                        user_found = True
                        if row['password_hash'] == password_hash:
                            row['last_login'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            login_success = True
                            print(f"✅ Welcome back, {username}!")
                            print(f"📅 Last login updated: {row['last_login']}")
                    users.append(row)
            
            if not user_found:
                print("❌ Username not found!")
                return
            if not login_success:
                print("❌ Invalid password!")
                return
            
            # Update CSV with new login time
            with open(self.csv_file, 'w', newline='') as file:
                if users:
                    writer = csv.DictWriter(file, fieldnames=users[0].keys())
                    writer.writeheader()
                    writer.writerows(users)
                    
        except Exception as e:
            print(f"❌ Login error: {e}")
    
    def view_users(self):
        """View all registered users (admin function)"""
        try:
            print("\n👥 ALL REGISTERED USERS")
            print("-" * 30)
            
            if not os.path.exists(self.csv_file):
                print("❌ No users found!")
                return
            
            with open(self.csv_file, 'r') as file:
                reader = csv.DictReader(file)
                users = list(reader)
                
                if not users:
                    print("❌ No users registered!")
                    return
                
                print(f"{'Username':<15} {'Created':<20} {'Last Login':<20}")
                print("=" * 55)
                
                for user in users:
                    print(f"{user['username']:<15} {user['created_date']:<20} {user['last_login']:<20}")
                    
                print(f"\n📊 Total Users: {len(users)}")
                
        except Exception as e:
            print(f"❌ Error viewing users: {e}")

def main():
    """Main program function"""
    auth = AuthSystem()
    
    print("=" * 50)
    print("🔐 USERNAME PASSWORD CHECKER SYSTEM")
    print("🏫 VNIT CSP300 - Software Lab III")
    print("👨‍💻 Assignment 2 - JIRA Integration Demo")
    print("=" * 50)
    
    while True:
        try:
            print("\n🎯 MAIN MENU")
            print("1️⃣  Register New User")
            print("2️⃣  Login")
            print("3️⃣  View All Users (Admin)")
            print("4️⃣  Exit")
            
            choice = input("\n➡️  Enter choice (1-4): ").strip()
            
            if choice == '1':
                auth.register_user()
            elif choice == '2':
                auth.login_user()
            elif choice == '3':
                auth.view_users()
            elif choice == '4':
                print("\n✅ Thank you for using the system!")
                print("🎓 VNIT CSP300 Assignment 2 Demo Complete")
                break
            else:
                print("❌ Invalid choice! Please select 1-4.")
                
        except KeyboardInterrupt:
            print("\n\n⚠️  Program interrupted by user")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
