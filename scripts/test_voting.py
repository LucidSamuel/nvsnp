#!/usr/bin/env python3

from interact import VotingInteraction
import unittest

class TestVoting(unittest.TestCase):
    def setUp(self):
        self.voting = VotingInteraction()
        
    def test_cast_vote(self):
        """Test voting functionality"""
        result = self.voting.cast_vote(1)
        self.assertTrue(result)
        
    def test_verify_vote(self):
        """Test vote verification"""
        result = self.voting.verify_vote(1)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
