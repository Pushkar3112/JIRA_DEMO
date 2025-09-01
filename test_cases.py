import unittest
import os
from main import UserPasswordChecker

class TestUserPasswordChecker(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.test_csv = "test_users.csv"
        self.checker = UserPasswordChecker(self.test_csv)
    
    def tearDown(self):
        """Clean up test files"""
        if os.path.exists(self.test_csv):
            os.remove(self.test_csv)
    
    def test_user_registration(self):
        """Test user registration functionality"""
        # Valid registration
        result = self.checker.register_user("testuser", "password123")
        self.assertIn("registered successfully", result)
        
        # Duplicate username
        result = self.checker.register_user("testuser", "password456")
        self.assertIn("already exists", result)
        
        # Invalid username length
        result = self.checker.register_user("ab", "password123")
        self.assertIn("at least 3 characters", result)
        
        # Invalid password length
        result = self.checker.register_user("validuser", "123")
        self.assertIn("at least 6 characters", result)
    
    def test_user_authentication(self):
        """Test user authentication functionality"""
        # Register a user first
        self.checker.register_user("authtest", "password123")
        
        # Valid login
        result = self.checker.authenticate_user("authtest", "password123")
        self.assertIn("Login successful", result)
        
        # Invalid password
        result = self.checker.authenticate_user("authtest", "wrongpassword")
        self.assertIn("Invalid password", result)
        
        # Non-existent user
        result = self.checker.authenticate_user("nonexistent", "password123")
        self.assertIn("not found", result)
        
        # Empty credentials
        result = self.checker.authenticate_user("", "")
        self.assertIn("cannot be empty", result)

if __name__ == "__main__":
    unittest.main()
