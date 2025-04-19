# Vedic Language Model (VLM)

A compact language model based on Vedic knowledge systems, Pāṇini's Aṣṭādhyāyī, and modern retrieval techniques.

## Project Structure

- **src/vlm/core**: Core LLM model architecture
- **src/vlm/grammar**: Grammar validation layer based on Aṣṭādhyāyī
- **src/vlm/reasoning**: Neuro-symbolic reasoning module
- **src/vlm/rag**: Retrieval-Augmented Generation engine
- **src/data**: Data processing and loading utilities
- **src/utils**: Shared utilities
- **src/evaluation**: Evaluation metrics and benchmarks
- **tests/**: Test suite for all components
- **data/**: Storage for datasets
- **notebooks/**: Jupyter notebooks for experiments

## Components

1. **Core LLM** (VLM Core):
   - Transformer-based encoder-decoder trained on the Vedas
   - Phonemic tokenization

2. **Grammar Validation Layer**:
   - Runtime application of Pāṇinian grammar rules
   - Rule-engine for syntax validation

3. **Neuro-Symbolic Reasoning Module**:
   - Śāstra-informed reasoning
   - Hybrid attention mechanisms

4. **RAG Engine**:
   - Dense retrieval from Indic knowledge bases
   - Context-aware generation

## Getting Started

```bash
# Clone the repository
git clone https://github.com/yourusername/vlm.git
cd vlm

# Set up environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run tests
python -m pytest
```
