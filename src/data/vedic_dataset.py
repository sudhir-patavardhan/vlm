from typing import Dict, List, Optional
import torch
from torch.utils.data import Dataset

class VedicDataset(Dataset):
    """Dataset for Vedic texts.
    
    This dataset class handles loading and preprocessing of Vedic texts
    for training the VLM model.
    """
    
    def __init__(self, texts: List[str], tokenizer, max_length: int = 512):
        """Initialize the dataset.
        
        Args:
            texts: List of text strings from Vedic sources
            tokenizer: Tokenizer for processing texts
            max_length: Maximum sequence length
        """
        self.texts = texts
        self.tokenizer = tokenizer
        self.max_length = max_length
        
    def __len__(self) -> int:
        """Get dataset length."""
        return len(self.texts)
    
    def __getitem__(self, idx: int) -> Dict[str, torch.Tensor]:
        """Get dataset item.
        
        Args:
            idx: Item index
            
        Returns:
            Dict of tensors for model input
        """
        text = self.texts[idx]
        
        # Tokenize the text
        encodings = self.tokenizer(text, 
                                  max_length=self.max_length,
                                  padding="max_length",
                                  truncation=True,
                                  return_tensors="pt")
        
        # Create inputs for causal language modeling
        input_ids = encodings["input_ids"].squeeze(0)
        attention_mask = encodings["attention_mask"].squeeze(0)
        
        # Labels are the input_ids shifted right (for causal LM)
        labels = input_ids.clone()
        
        return {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "labels": labels
        }
