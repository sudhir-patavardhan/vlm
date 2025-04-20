#!/usr/bin/env python
"""
Test script for the Sanskrit tokenizer and sandhi processor.
"""

import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.vlm.core.tokenizer import SanskritTokenizer
from src.vlm.grammar.sandhi import SandhiProcessor

def test_sandhi_processor():
    """Test the sandhi processor functionality."""
    print("Testing Sandhi Processor...")
    processor = SandhiProcessor()
    
    # Test sandhi application
    test_cases = [
        ("rama", "iva", "rameva"),  # a + i = e
        ("deva", "atra", "devātra"),  # a + a = ā
        ("gaccha", "uta", "gacchota"),  # a + u = o
    ]
    
    for first, second, expected in test_cases:
        result = processor.apply(first, second)
        print(f"Sandhi Application: {first} + {second} = {result}")
        print(f"Expected: {expected}")
        print(f"Correct: {result == expected}")
        print()
    
    # Test sandhi reversal
    test_cases = [
        ("devātra", ["deva", "atra"]),  # ā = a + a
        ("rameva", ["rama", "iva"]),  # e = a + i
        ("gacchota", ["gaccha", "uta"]),  # o = a + u
    ]
    
    for combined, expected in test_cases:
        result = processor.reverse(combined)
        print(f"Sandhi Reversal: {combined} = {result}")
        print(f"Expected: {expected}")
        print(f"Correct: {set(result) == set(expected)}")
        print()

def test_tokenizer():
    """Test the Sanskrit tokenizer functionality."""
    print("Testing Sanskrit Tokenizer...")
    tokenizer = SanskritTokenizer()
    
    # Test simple tokenization
    test_cases = [
        "नमस्ते",  # Namaste
        "रामः वनं गच्छति",  # Rama goes to the forest
        "अग्निमीळे पुरोहितम्",  # First verse of Rigveda
    ]
    
    for text in test_cases:
        tokens = tokenizer._tokenize(text)
        token_ids = [tokenizer._convert_token_to_id(token) for token in tokens]
        reconstructed = tokenizer.convert_tokens_to_string(tokens)
        
        print(f"Text: {text}")
        print(f"Tokens: {tokens}")
        print(f"Token IDs: {token_ids}")
        print(f"Reconstructed: {reconstructed}")
        print()

if __name__ == "__main__":
    print("=" * 50)
    print("Sanskrit NLP Tools Test")
    print("=" * 50)
    print()
    
    test_sandhi_processor()
    print("=" * 50)
    test_tokenizer()