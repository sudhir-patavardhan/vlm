class SandhiProcessor:
    """Processor for Sanskrit sandhi (phonological junction) rules.
    
    Handles the application and reversal of sandhi rules in Sanskrit text,
    which are essential for both tokenization and generation.
    """
    
    def __init__(self):
        """Initialize the sandhi processor with rule sets."""
        # Define common sandhi rules for reversal (splitting)
        # Format: {result_pattern: [(first_part_pattern, second_part_pattern), ...]}
        self.vowel_sandhi_rules = {
            'ā': [('a', 'a')],
            'ai': [('a', 'e'), ('a', 'i')],
            'au': [('a', 'o'), ('a', 'u')],
            'ī': [('i', 'i')],
            'ū': [('u', 'u')],
            'e': [('a', 'i')],
            'o': [('a', 'u')],
        }
        
        self.visarga_sandhi_rules = {
            'o': [('aḥ', '')],
            'ss': [('s', 's')],
            'śc': [('s', 'c')],
            'ṣṭ': [('s', 'ṭ')],
        }
        
        # Rules for consonant sandhi
        self.consonant_sandhi_rules = {
            'nn': [('t', 'n')],
            'ñc': [('n', 'c')],
            'ṅg': [('n', 'g')],
            'ṇṭ': [('n', 'ṭ')],
            'cc': [('t', 'c')],
            'jj': [('t', 'j')],
            'ṭṭ': [('t', 'ṭ')],
            'dd': [('t', 'd')],
        }
        
        # Combine all rules
        self.rules = {}
        self.rules.update(self.vowel_sandhi_rules)
        self.rules.update(self.visarga_sandhi_rules)
        self.rules.update(self.consonant_sandhi_rules)
        
        # Sanskrit word boundary markers
        self.word_endings = ['aḥ', 'am', 'ām', 'a', 'i', 'ī', 'u', 'ū', 'e', 'o']
        
    def apply(self, text1, text2):
        """Apply sandhi rules to join two text segments.
        
        Args:
            text1: First text segment
            text2: Second text segment
            
        Returns:
            str: Combined text with sandhi rules applied
        """
        # Basic implementation of sandhi application
        if not text1 or not text2:
            return text1 + text2
            
        # Get the last character of text1 and first character of text2
        last_char = text1[-1]
        first_char = text2[0] if text2 else ''
        
        # Check for vowel sandhi (a + a = ā)
        if last_char == 'a' and first_char == 'a':
            return text1[:-1] + 'ā' + text2[1:]
        
        # Check for vowel sandhi (a + i = e)
        elif last_char == 'a' and first_char == 'i':
            return text1[:-1] + 'e' + text2[1:]
        
        # Check for vowel sandhi (a + u = o)
        elif last_char == 'a' and first_char == 'u':
            return text1[:-1] + 'o' + text2[1:]
        
        # Default: just concatenate
        return text1 + text2
    
    def reverse(self, combined_text):
        """Split text by reversing sandhi rules.
        
        Args:
            combined_text: Text with sandhi combinations
            
        Returns:
            list: Component segments after sandhi reversal
        """
        # Basic sandhi splitting implementation
        # For a proper implementation, we would need a more sophisticated
        # algorithm that considers all possible splits and chooses the most likely ones
        
        # For now, we'll just look for potential sandhi boundaries and try to split
        # based on the most common rules
        
        result = []
        current_word = ""
        
        for i in range(len(combined_text)):
            current_word += combined_text[i]
            
            # Check if we're at a potential word boundary
            for ending in self.word_endings:
                if current_word.endswith(ending):
                    # Check if this could be a sandhi boundary
                    for j in range(max(0, len(current_word) - 3), len(current_word)):
                        substring = current_word[j:]
                        # Look for known sandhi patterns
                        for result_pattern, replacements in self.rules.items():
                            if substring.endswith(result_pattern):
                                # Found a potential sandhi boundary
                                result.append(current_word)
                                current_word = ""
                                break
                    
                    if current_word == "":
                        break
        
        # Add any remaining text
        if current_word:
            result.append(current_word)
        
        # If we couldn't split, return the original text
        if not result:
            return [combined_text]
            
        return result
    
    def identify_possible_splits(self, text):
        """Identify all possible sandhi split points in a text.
        
        Args:
            text: The text to analyze
            
        Returns:
            list: List of (position, possible_splits) tuples where possible_splits
                 is a list of (first_part, second_part) tuples
        """
        possible_splits = []
        
        # Scan the text for potential sandhi points
        for i in range(1, len(text) - 1):
            # Check for each sandhi pattern
            for pattern, replacements in self.rules.items():
                # If we find a pattern at the current position
                if text[i-len(pattern)+1:i+1] == pattern:
                    splits = []
                    for first, second in replacements:
                        splits.append((
                            text[:i-len(pattern)+1] + first,
                            second + text[i+1:]
                        ))
                    if splits:
                        possible_splits.append((i, splits))
        
        return possible_splits