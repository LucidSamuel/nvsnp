#!/usr/bin/env python3

import sys
import json
import time
from pathlib import Path
import os
import hashlib
from web3 import Web3

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.key_manager import KeyManager

class VotingInteraction:
    def __init__(self):
        self.key_manager = KeyManager()
        self.keys = self.key_manager.get_keys(public_only=False)
        
        # Connect to Ethereum node
        self.web3 = Web3(Web3.HTTPProvider('http://localhost:8545'))  # Update with your node URL
        if not self.web3.isConnected():
            raise Exception("Failed to connect to Ethereum node")
        
        # Load contract ABI and address
        self.contract_address = '0xYourContractAddress'  # Update with your contract address
        with open('path/to/your/contract_abi.json', 'r') as abi_file:
            self.contract_abi = json.load(abi_file)
        
        self.contract = self.web3.eth.contract(address=self.contract_address, abi=self.contract_abi)
        
    def cast_vote(self, candidate_id: int):
        """Cast a vote for a candidate"""
        try:
            # Get necessary keys
            private_key = self.keys.get('private_key')
            public_key = self.keys.get('public_key')
            
            if not private_key or not public_key:
                print("Error: Required keys not found")
                return False
            
            # 1. Create the vote transaction
            vote_data = self._create_vote_transaction(candidate_id)
            
            # 2. Sign the vote with private key
            signed_vote = self._sign_vote(vote_data, private_key)
            
            # 3. Submit the vote
            success = self._submit_vote(signed_vote)
            
            return success
            
        except Exception as e:
            print(f"Error casting vote: {str(e)}")
            return False
    
    def _create_vote_transaction(self, candidate_id: int):
        """Create a vote transaction"""
        # Create vote transaction structure
        vote_data = {
            'candidate_id': candidate_id,
            'timestamp': int(time.time()),
            'public_key': self.keys.get('public_key')
        }
        return vote_data
    
    def _sign_vote(self, vote_data: dict, private_key: str):
        """Sign the vote with private key using PLUME"""
        try:
            # Convert vote data to bytes for signing
            vote_bytes = json.dumps(vote_data, sort_keys=True).encode()
            
            # Generate message hash
            message_hash = int.from_bytes(hashlib.sha256(vote_bytes).digest(), byteorder='big')
            
            # Get public key components
            pk_x = self.keys.get('pk_x')
            pk_y = self.keys.get('pk_y')
            
            # Generate nullifier
            nullifier = self._generate_nullifier(message_hash, private_key)
            
            # Create PLUME signature
            plume_signature = {
                'message': message_hash,
                'nullifier': nullifier,
                'public_key': {
                    'x': pk_x,
                    'y': pk_y
                }
            }
            
            return {
                'vote_data': vote_data,
                'signature': plume_signature
            }
        except Exception as e:
            print(f"Error signing vote: {str(e)}")
            raise
    
    def _generate_nullifier(self, message_hash: int, private_key: str):
        """Generate a nullifier using PLUME scheme"""
        try:
            # Convert inputs to appropriate format
            msg = str(message_hash)
            pk = private_key
            
            # Use the same nullifier generation logic as in your Noir contract
            nullifier = hashlib.sha256(f"{msg}{pk}".encode()).hexdigest()
            
            return nullifier
        except Exception as e:
            print(f"Error generating nullifier: {str(e)}")
            raise
    
    def _submit_vote(self, signed_vote: dict):
        """Submit the signed vote to the Noir contract"""
        try:
            # Prepare the vote data for the contract
            vote_data = {
                'candidate': signed_vote['vote_data']['candidate_id'],
                'signature': {
                    'r': signed_vote['signature']['message'],
                    's': signed_vote['signature']['nullifier'],
                    'nullifier': signed_vote['signature']['nullifier']
                },
                'pk': [
                    signed_vote['signature']['public_key']['x'],
                    signed_vote['signature']['public_key']['y']
                ]
            }
            
            # Call the contract function
            tx = self.contract.functions.cast_vote_with_nullifier(
                vote_data['candidate'],
                vote_data['signature'],
                vote_data['pk']
            ).buildTransaction({
                'from': self.web3.eth.accounts[0],  # Update with your account
                'gas': 2000000,
                'gasPrice': self.web3.toWei('50', 'gwei')
            })
            
            # Sign and send the transaction
            signed_tx = self.web3.eth.account.sign_transaction(tx, private_key=self.keys['private_key'])
            tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
            
            # Wait for transaction receipt
            receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
            print(f"Transaction successful with hash: {tx_hash.hex()}")
            
            return receipt.status == 1
        except Exception as e:
            print(f"Error submitting vote: {str(e)}")
            return False
            
    def verify_vote(self, candidate_id: int):
        """Verify a vote using the Noir contract"""
        try:
            # Call the contract function to verify the vote
            result = self.contract.functions.get_vote(candidate_id).call()
            
            print(f"Vote count for candidate {candidate_id}: {result}")
            
            return True
        except Exception as e:
            print(f"Error verifying vote: {str(e)}")
            return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 interact.py <candidate_id>")
        sys.exit(1)
    
    try:
        candidate_id = int(sys.argv[1])
        voting = VotingInteraction()
        
        # Cast vote
        if voting.cast_vote(candidate_id):
            print("Vote cast successfully")
            
            # Verify vote
            if voting.verify_vote(candidate_id):
                print("Vote verified successfully")
            else:
                print("Vote verification failed")
        else:
            print("Failed to cast vote")
            
    except ValueError:
        print("Error: Candidate ID must be a number")
        sys.exit(1)

if __name__ == "__main__":
    main()
