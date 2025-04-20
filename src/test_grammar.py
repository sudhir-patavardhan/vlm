#!/usr/bin/env python
"""
Test script for the Aṣṭādhyāyī grammar engine.
"""

import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.vlm.grammar.ashtadhyayi import AshtadhyayiEngine

def test_grammar_validation():
    """Test grammar validation functionality."""
    print("Testing Grammar Validation...")
    engine = AshtadhyayiEngine()
    
    # Test valid sentences
    valid_sentences = [
        "rāmaḥ vanam gacchati",  # Rama goes to the forest
        "devāḥ yajñam rakṣanti",  # The gods protect the sacrifice
        "aham pustakam paṭhāmi",  # I read the book
    ]
    
    for sentence in valid_sentences:
        is_valid = engine.validate(sentence)
        print(f"Sentence: {sentence}")
        print(f"Valid: {is_valid}")
        print()
    
    # Test invalid sentences
    invalid_sentences = [
        "rāma vanam gacchati",  # Missing visarga on subject
        "rāmaḥ vanam",  # Missing verb
        "gacchati rāmaḥ vanam",  # Wrong word order (VSO instead of SOV)
    ]
    
    for sentence in invalid_sentences:
        is_valid = engine.validate(sentence)
        corrected = engine.correct(sentence)
        print(f"Invalid Sentence: {sentence}")
        print(f"Valid: {is_valid}")
        print(f"Corrected: {corrected}")
        print()

def test_sentence_parsing():
    """Test sentence parsing functionality."""
    print("Testing Sentence Parsing...")
    engine = AshtadhyayiEngine()
    
    # Test sentence parsing
    test_sentences = [
        "rāmaḥ vanam gacchati",  # Rama goes to the forest
        "sītā phalam khadati",  # Sita eats the fruit
    ]
    
    for sentence in test_sentences:
        analysis = engine.parse_sentence(sentence)
        print(f"Sentence: {sentence}")
        print("Analysis:")
        for i, word_analysis in enumerate(analysis["words"]):
            print(f"  Word {i+1}: {word_analysis['text']}")
            for key, value in word_analysis.items():
                if key != "text":
                    print(f"    {key}: {value}")
        print()

if __name__ == "__main__":
    print("=" * 50)
    print("Aṣṭādhyāyī Grammar Engine Test")
    print("=" * 50)
    print()
    
    test_grammar_validation()
    print("=" * 50)
    test_sentence_parsing()