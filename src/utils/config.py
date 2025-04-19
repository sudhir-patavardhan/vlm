from dataclasses import dataclass
from typing import Optional, List, Dict, Any

@dataclass
class VLMConfig:
    """Configuration for Vedic Language Model.
    
    This class holds all configuration parameters for the VLM components.
    """
    
    # Model architecture
    hidden_size: int = 768
    num_hidden_layers: int = 12
    num_attention_heads: int = 12
    intermediate_size: int = 3072
    hidden_dropout_prob: float = 0.1
    attention_probs_dropout_prob: float = 0.1
    
    # Tokenizer
    vocab_size: int = 50000
    max_position_embeddings: int = 512
    
    # Training
    learning_rate: float = 5e-5
    weight_decay: float = 0.01
    adam_epsilon: float = 1e-8
    warmup_steps: int = 0
    max_grad_norm: float = 1.0
    num_train_epochs: int = 3
    
    # Grammar validation
    enable_grammar_validation: bool = True
    grammar_rules_path: Optional[str] = None
    
    # RAG
    retriever_index_path: Optional[str] = None
    num_retrieval_docs: int = 5
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {k: v for k, v in self.__dict__.items()}
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'VLMConfig':
        """Create from dictionary."""
        return cls(**config_dict)
