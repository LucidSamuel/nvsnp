import secrets
import hashlib
from config.key_manager import KeyManager
import os
from typing import Dict

def generate_secure_key() -> str:
    """Generate a cryptographically secure key"""
    return secrets.token_hex(32)

def generate_keys() -> Dict[str, str]:
    """Generate keys without hardcoding any values"""
    try:
        # Generate keys securely
        private_key = generate_secure_key()
        
        # In a real implementation, you would derive these from the private key
        # using proper elliptic curve operations
        # This is just a placeholder for demonstration
        public_key_x = generate_secure_key()
        public_key_y = generate_secure_key()
        
        # Combine x and y coordinates for the full public key
        public_key = f"{public_key_x},{public_key_y}"
        
        keys = {
            'private_key': private_key,
            'public_key': public_key,
            'pk_x': public_key_x,
            'pk_y': public_key_y
        }
        
        # Store keys securely
        key_manager = KeyManager()
        key_manager.store_generated_keys(keys)
        
        # Print only public information
        print("Keys generated and stored securely.")
        print(f"Public Key: {public_key}")
        
        return keys
        
    except Exception as e:
        print(f"Error generating keys: {str(e)}")
        return {}

if __name__ == "__main__":
    generate_keys()