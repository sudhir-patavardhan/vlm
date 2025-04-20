class AshtadhyayiEngine:
    """Implementation of Pāṇini's Aṣṭādhyāyī grammar system.
    
    This engine implements the rule-based grammar of Sanskrit as codified
    in the Aṣṭādhyāyī, for validating and correcting text generations.
    """
    
    def __init__(self):
        """Initialize rule engine with Aṣṭādhyāyī rules."""
        # Initialize rule dictionaries
        self.rules = {}
        self.meta_rules = {}
        
        # Initialize basic Aṣṭādhyāyī rules
        self._initialize_rules()
    
    def _initialize_rules(self):
        """Initialize the basic set of Aṣṭādhyāyī rules."""
        # In a full implementation, these would be loaded from a comprehensive rule base
        # For now, we'll implement a subset of rules as a proof of concept
        
        # Sandhi rules (1.1.1 - 1.1.8)
        self.rules["sandhi"] = {
            "vowel_sandhi": [
                # Rule: a/ā + a/ā = ā
                {"pattern": r"([aā])([aā])", "replacement": r"ā"},
                # Rule: a/ā + i/ī = e
                {"pattern": r"([aā])([iī])", "replacement": r"e"},
                # Rule: a/ā + u/ū = o
                {"pattern": r"([aā])([uū])", "replacement": r"o"},
            ],
            "visarga_sandhi": [
                # Rule: aḥ + vowel = o
                {"pattern": r"aḥ([aeiouāīūṛṝḷḹ])", "replacement": r"o\1"},
                # Rule: āḥ + vowel = ā
                {"pattern": r"āḥ([aeiouāīūṛṝḷḹ])", "replacement": r"ā\1"},
            ]
        }
        
        # Case endings (Vibhakti) rules (2.1 - 2.4)
        self.rules["case_endings"] = {
            "masculine": {
                # Nominative singular
                "nom_sg": {"pattern": r"a$", "replacement": r"aḥ"},
                # Accusative singular
                "acc_sg": {"pattern": r"a$", "replacement": r"am"},
                # Instrumental singular
                "ins_sg": {"pattern": r"a$", "replacement": r"ena"},
            },
            "feminine": {
                # Nominative singular
                "nom_sg": {"pattern": r"ā$", "replacement": r"ā"},
                # Accusative singular
                "acc_sg": {"pattern": r"ā$", "replacement": r"ām"},
                # Instrumental singular
                "ins_sg": {"pattern": r"ā$", "replacement": r"ayā"},
            }
        }
        
        # Verb conjugation rules (3.1 - 3.4)
        self.rules["verb_conjugation"] = {
            "present_tense": {
                # 3rd person singular 
                "3sg": {"pattern": r"([a-zA-Z]+)", "replacement": r"\1ti"},
                # 3rd person plural
                "3pl": {"pattern": r"([a-zA-Z]+)", "replacement": r"\1nti"},
            }
        }
        
        # Meta-rules (Paribhāṣā)
        self.meta_rules = {
            # Rule of proximity - apply closest rule first
            "proximity": {"priority": 1},
            # Rule of specificity - more specific rule wins
            "specificity": {"priority": 2},
        }
    
    def validate(self, text):
        """Validate a generated text against Pāṇinian grammar rules.
        
        Args:
            text: The text to validate
            
        Returns:
            bool: Whether the text is grammatically valid
        """
        # In a full implementation, this would perform comprehensive grammatical validation
        # For now, we'll implement some basic checks
        
        # Check for basic sentence structure (subject-object-verb)
        # Sanskrit is primarily SOV language
        words = text.split()
        
        # Very basic check: if there are 3+ words, check if the last one ends with 'ti' (common verb ending)
        if len(words) >= 3:
            # Check if last word looks like a verb (ends with ti/nti for present tense)
            last_word = words[-1]
            if last_word.endswith('ti') or last_word.endswith('nti'):
                # Check if there's a word that looks like a subject (ends with ḥ for masculine nominative)
                potential_subject = False
                for word in words[:-1]:
                    if word.endswith('ḥ') or word.endswith('m'):
                        potential_subject = True
                        break
                
                if potential_subject:
                    return True
        
        # Fallback to a simpler validation for short phrases
        if len(words) <= 2:
            # For short phrases, we'll just check if they make sense as fragments
            valid_endings = ['ḥ', 'm', 'ām', 'ā', 'ti', 'nti']
            for word in words:
                for ending in valid_endings:
                    if word.endswith(ending):
                        return True
        
        # If no valid structure was found
        return False
    
    def correct(self, text):
        """Apply grammar rules to correct a text if invalid.
        
        Args:
            text: The text to correct
            
        Returns:
            str: The corrected text
        """
        # In a full implementation, this would apply grammar rules to fix issues
        # For now, we'll implement some basic corrections
        
        words = text.split()
        
        # Simple rule: if the last word doesn't look like a verb, 
        # find a word that might be a verb and move it to the end
        if len(words) >= 2:
            last_word = words[-1]
            if not (last_word.endswith('ti') or last_word.endswith('nti')):
                for i, word in enumerate(words[:-1]):
                    if word.endswith('ti') or word.endswith('nti'):
                        # Move verb to the end
                        verb = words.pop(i)
                        words.append(verb)
                        break
        
        # Apply case correction: ensure nouns have proper endings
        for i, word in enumerate(words):
            # Check for neuter words missing visarga
            if word.endswith('a') and i < len(words) - 1:  # Not the verb
                words[i] = word + 'ḥ'  # Add visarga for nominative case
        
        return ' '.join(words)

    def parse_sentence(self, text):
        """Parse a Sanskrit sentence into its grammatical components.
        
        Args:
            text: The text to parse
            
        Returns:
            dict: A dictionary with the grammatical analysis
        """
        # This would be a complex implementation in a full engine
        # For now, we'll provide a simplified parsing
        
        words = text.split()
        analysis = {
            "sentence": text,
            "words": [],
        }
        
        for word in words:
            word_analysis = {"text": word}
            
            # Simple part-of-speech detection
            if word.endswith('ti') or word.endswith('nti'):
                word_analysis["pos"] = "verb"
                word_analysis["tense"] = "present"
                if word.endswith('nti'):
                    word_analysis["number"] = "plural"
                else:
                    word_analysis["number"] = "singular"
            
            elif word.endswith('ḥ'):
                word_analysis["pos"] = "noun"
                word_analysis["case"] = "nominative"
                word_analysis["gender"] = "masculine"
            
            elif word.endswith('m'):
                word_analysis["pos"] = "noun"
                word_analysis["case"] = "accusative"
            
            else:
                word_analysis["pos"] = "unknown"
            
            analysis["words"].append(word_analysis)
        
        return analysis