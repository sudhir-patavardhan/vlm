from typing import Dict, List, Optional, Set, Union
import re
import os
from transformers import PreTrainedTokenizer

from src.vlm.grammar.sandhi import SandhiProcessor

class SanskritTokenizer(PreTrainedTokenizer):
    """Specialized tokenizer for Sanskrit text with phonemic awareness.
    
    This tokenizer implements phonemic tokenization for Sanskrit, respecting
    the special characteristics of Vedic texts including accent marks,
    phonological rules, and sandhi patterns.
    """
    
    model_input_names = ["input_ids", "attention_mask"]
    
    def __init__(
        self,
        vocab_file=None,
        unk_token="<unk>",
        sep_token="</s>",
        pad_token="<pad>",
        cls_token="<s>",
        mask_token="<mask>",
        **kwargs
    ):
        """Initialize the tokenizer.
        
        Args:
            vocab_file: Optional path to a vocabulary file
        """
        # Initialize sandhi processor
        self.sandhi_processor = SandhiProcessor()
        
        # Sanskrit phonemes and phonetic categories
        # (In a full implementation, these would be much more comprehensive)
        self.vowels = ['a', 'ā', 'i', 'ī', 'u', 'ū', 'e', 'ai', 'o', 'au', 'ṛ', 'ṝ', 'ḷ', 'ḹ']
        self.consonants = [
            'k', 'kh', 'g', 'gh', 'ṅ',
            'c', 'ch', 'j', 'jh', 'ñ',
            'ṭ', 'ṭh', 'ḍ', 'ḍh', 'ṇ',
            't', 'th', 'd', 'dh', 'n',
            'p', 'ph', 'b', 'bh', 'm',
            'y', 'r', 'l', 'v',
            'ś', 'ṣ', 's', 'h'
        ]
        
        # Vedic accents and special characters
        self.accents = ['॒', '॑', '᳚', '᳛']  # Svarita, Udātta, etc.
        self.special_chars = ['ṃ', 'ḥ', '।', '॥']  # Anusvāra, Visarga, daṇḍa, etc.
        
        # Define vocab dictionary
        self.vocab = {}
        self.ids_to_tokens = {}
        
        # Build vocabulary
        self._create_vocab()
        
        # Standard transformers init
        super().__init__(
            unk_token=unk_token,
            sep_token=sep_token,
            pad_token=pad_token,
            cls_token=cls_token,
            mask_token=mask_token,
            **kwargs
        )
        
        # Regex pattern for basic Sanskrit tokenization
        self.sanskrit_pattern = re.compile(r'([{}])|([{}])'.format(
            ''.join(self.vowels + self.accents + self.special_chars),
            ''.join(self.consonants)
        ))
    
    def _create_vocab(self):
        """Create the vocabulary."""
        # Special tokens
        tokens = ["<pad>", "<s>", "</s>", "<unk>", "<mask>"]
        
        # Add phonemes to vocabulary
        tokens.extend(self.vowels)
        tokens.extend(self.consonants)
        tokens.extend(self.accents)
        tokens.extend(self.special_chars)
        
        # Create vocab dictionaries
        for i, token in enumerate(tokens):
            self.vocab[token] = i
            self.ids_to_tokens[i] = token
    
    @property
    def vocab_size(self) -> int:
        """Get the vocabulary size."""
        return len(self.vocab)
    
    def get_vocab(self) -> Dict[str, int]:
        """Get the vocabulary dictionary."""
        return self.vocab.copy()
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize Sanskrit text into phonemic units.
        
        This implementation follows these steps:
        1. Apply sandhi splitting to separate compound words
        2. Tokenize each word into phonemic units
        3. Return the flattened list of tokens
        
        Args:
            text: Input Sanskrit text
            
        Returns:
            List of tokens
        """
        # First, try to split by sandhi rules
        words = self.sandhi_processor.reverse(text)
        
        # Then tokenize each word into phonemic units
        tokens = []
        for word in words:
            # Apply basic phonemic tokenization
            word_tokens = self._tokenize_word(word)
            tokens.extend(word_tokens)
        
        return tokens
    
    def _tokenize_word(self, word: str) -> List[str]:
        """Tokenize a single Sanskrit word into phonemic units.
        
        Args:
            word: A Sanskrit word
            
        Returns:
            List of phonemic tokens
        """
        # For now, use a simple character-based tokenization
        # In a full implementation, we would handle consonant clusters, etc.
        return list(word)
    
    def _convert_token_to_id(self, token: str) -> int:
        """Convert token to vocabulary ID."""
        return self.vocab.get(token, self.vocab.get("<unk>"))
    
    def _convert_id_to_token(self, index: int) -> str:
        """Convert vocabulary ID to token."""
        return self.ids_to_tokens.get(index, "<unk>")
    
    def convert_tokens_to_string(self, tokens: List[str]) -> str:
        """Convert a list of tokens back to a string."""
        # For Sanskrit, we need to handle sandhi when combining tokens
        if not tokens:
            return ""
        
        text = tokens[0]
        for token in tokens[1:]:
            # Apply sandhi rules when combining tokens
            text = self.sandhi_processor.apply(text, token)
        
        return text
    
    def save_vocabulary(self, save_directory: str, filename_prefix: Optional[str] = None) -> List[str]:
        """Save the vocabulary to a file."""
        if not os.path.isdir(save_directory):
            raise ValueError(f"Vocabulary path ({save_directory}) should be a directory")
        
        vocab_file = os.path.join(
            save_directory, (filename_prefix + "-" if filename_prefix else "") + "vocab.txt"
        )
        
        with open(vocab_file, "w", encoding="utf-8") as f:
            for token, index in sorted(self.vocab.items(), key=lambda x: x[1]):
                f.write(token + "\n")
        
        return [vocab_file]
    
    def build_inputs_with_special_tokens(self, token_ids_0, token_ids_1=None):
        """Build model inputs from a sequence by appending special tokens."""
        if token_ids_1 is None:
            return [self.cls_token_id] + token_ids_0 + [self.sep_token_id]
        cls = [self.cls_token_id]
        sep = [self.sep_token_id]
        return cls + token_ids_0 + sep + token_ids_1 + sep