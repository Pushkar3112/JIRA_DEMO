import hashlib
from datetime import datetime
import csv
import os

class UserPasswordChecker:
    def __init__(self, csv_file="users.csv"):
        self.csv_file = csv_file
        # Create CSV file if it doesn't exist
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['username', 'password_hash', 'created_date'])
    
    def hash_password(self, password):
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def get_users(self):
        """Read users from CSV file"""
        users = {}
        try:
            with open(self.csv_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    users[row['username']] = {
                        'password_hash': row['password_hash'],
                        'created_date': row['created_date']
                    }
        except Exception as e:
            print(f"Error reading CSV: {str(e)}")
        return users
    
    def save_user(self, username, password_hash):
        """Save user to CSV file"""
        try:
            with open(self.csv_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([username, password_hash, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
            return True
        except Exception as e:
            print(f"Error writing to CSV: {str(e)}")
            return False
    
    def register_user(self, username, password):
        """Register new user with validation"""
        try:
            if len(username) < 3:
                raise ValueError("Username must be at least 3 characters long")
            
            if len(password) < 6:
                raise ValueError("Password must be at least 6 characters long")
            
            users = self.get_users()
            if username in users:
                raise ValueError(f"Username '{username}' already exists")
            
            if self.save_user(username, self.hash_password(password)):
                return f"User '{username}' registered successfully!"
            else:
                raise Exception("Failed to save user data")
            
        except ValueError as e:
            return f"Registration Error: {str(e)}"
        except Exception as e:
            return f"System Error: {str(e)}"
    
    def authenticate_user(self, username, password):
        """Authenticate user credentials"""
        try:
            if not username or not password:
                raise ValueError("Username and password cannot be empty")
            
            users = self.get_users()
            if username not in users:
                raise ValueError(f"Username '{username}' not found")
            
            password_hash = self.hash_password(password)
            
            if users[username]['password_hash'] == password_hash:
                return f"Login successful! Welcome {username}"
            else:
                raise ValueError("Invalid password")
                
        except ValueError as e:
            return f"Authentication Error: {str(e)}"
        except Exception as e:
            return f"System Error: {str(e)}"
    
    def list_users(self):
        """List all registered users"""
        users = self.get_users()
        if not users:
            return "No users registered yet."
        
        result = "Registered Users:\n"
        for username, data in users.items():
            result += f"- Username: {username}, Created: {data['created_date']}\n"
        return result

def run_tests():
    """Run basic test cases"""
    checker = UserPasswordChecker()
    
    # Test registration
    print("\nTesting Registration:")
    print(checker.register_user("test1", "password123"))
    print(checker.register_user("test1", "password123"))  # Should fail - duplicate
    print(checker.register_user("t", "pass"))  # Should fail - short username
    print(checker.register_user("test2", "pass"))  # Should fail - short password
    
    # Test authentication
    print("\nTesting Authentication:")
    print(checker.authenticate_user("test1", "password123"))  # Should succeed
    print(checker.authenticate_user("test1", "wrongpass"))  # Should fail
    print(checker.authenticate_user("nonexistent", "pass"))  # Should fail
    
    # Test user listing
    print("\nTesting User Listing:")
    print(checker.list_users())

def main():
    """Main function with user interface"""
    checker = UserPasswordChecker()
    
    while True:
        print("\n=== Username-Password Checker ===")
        print("1. Register New User")
        print("2. Login")
        print("3. List Users")
        print("4. Run Tests")
        print("5. Exit")
        
        try:
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == '1':
                print("\n--- User Registration ---")
                username = input("Enter username: ").strip()
                password = input("Enter password: ").strip()
                result = checker.register_user(username, password)
                print(result)
                
            elif choice == '2':
                print("\n--- User Login ---")
                username = input("Enter username: ").strip()
                password = input("Enter password: ").strip()
                result = checker.authenticate_user(username, password)
                print(result)
                
            elif choice == '3':
                print("\n--- Registered Users ---")
                print(checker.list_users())
                    
            elif choice == '4':
                print("\n--- Running Tests ---")
                run_tests()
                
            elif choice == '5':
                print("Thank you for using Username-Password Checker!")
                break
                
            else:
                print("Invalid choice. Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\n\nProgram interrupted by user.")
            break
        except Exception as e:
            print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
