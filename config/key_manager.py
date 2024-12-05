from dotenv import load_dotenv
import os
import json
from pathlib import Path
from typing import Dict, Optional

class KeyManager:
    def __init__(self):
        self.config_dir = Path('config')
        self.env_path = self.config_dir / '.env'
        self._ensure_config_dir()
        load_dotenv(self.env_path)
    
    def _ensure_config_dir(self) -> None:
        """Ensure config directory exists with proper permissions"""
        self.config_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
        
    def _secure_file_permissions(self) -> None:
        """Set secure file permissions for .env file"""
        if os.name != 'nt':  # For Unix-like systems
            os.chmod(self.env_path, 0o600)
    
    def store_generated_keys(self, keys_dict: Dict[str, str]) -> None:
        """Securely store generated keys"""
        try:
            with open(self.env_path, 'w') as f:
                for key, value in keys_dict.items():
                    f.write(f'{key.upper()}={value}\n')
            self._secure_file_permissions()
        except Exception as e:
            print(f"Error storing keys: {str(e)}")
            raise
    
    def get_keys(self, public_only: bool = True) -> Dict[str, Optional[str]]:
        """Retrieve stored keys, optionally only public ones"""
        keys = {}
        if public_only:
            # Only return public information
            keys['public_key'] = os.getenv('PUBLIC_KEY')
            keys['pk_x'] = os.getenv('PK_X')
            keys['pk_y'] = os.getenv('PK_Y')
        else:
            # Return all keys (use with caution)
            keys['private_key'] = os.getenv('PRIVATE_KEY')
            keys['public_key'] = os.getenv('PUBLIC_KEY')
            keys['pk_x'] = os.getenv('PK_X')
            keys['pk_y'] = os.getenv('PK_Y')
        return keys
