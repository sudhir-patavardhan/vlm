import argparse
import os
import torch
from torch.utils.data import DataLoader
from transformers import AdamW, get_linear_schedule_with_warmup

from vlm.core.model import VLMCore
from vlm.core.tokenizer import SanskritTokenizer
from data.vedic_dataset import VedicDataset
from data.processor import VedicTextProcessor
from utils.config import VLMConfig

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Train the Vedic Language Model")
    parser.add_argument(
        "--config", type=str, default="config.json", help="Path to config file"
    )
    parser.add_argument(
        "--data_dir", type=str, default="data/vedas", help="Directory with training data"
    )
    parser.add_argument(
        "--output_dir", type=str, default="models", help="Output directory for model"
    )
    parser.add_argument(
        "--batch_size", type=int, default=8, help="Batch size for training"
    )
    parser.add_argument(
        "--epochs", type=int, default=3, help="Number of training epochs"
    )
    return parser.parse_args()

def load_data(data_dir, tokenizer, max_length=512, batch_size=8):
    """Load and prepare training data."""
    # TODO: Implement data loading from Vedic texts
    # For now, use dummy text for structure
    texts = ["Sample Vedic text" for _ in range(10)]
    
    # Create dataset and dataloader
    dataset = VedicDataset(texts, tokenizer, max_length)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    
    return dataloader

def train(model, dataloader, config, output_dir):
    """Train the VLM model."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    
    # Setup optimizer and scheduler
    optimizer = AdamW(
        model.parameters(),
        lr=config.learning_rate,
        eps=config.adam_epsilon,
        weight_decay=config.weight_decay
    )
    
    total_steps = len(dataloader) * config.num_train_epochs
    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=config.warmup_steps,
        num_training_steps=total_steps
    )
    
    # Training loop
    for epoch in range(config.num_train_epochs):
        model.train()
        total_loss = 0
        
        for batch in dataloader:
            # Move batch to device
            batch = {k: v.to(device) for k, v in batch.items()}
            
            # Forward pass
            outputs = model(**batch)
            loss = outputs.loss
            
            # Backward pass
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), config.max_grad_norm)
            
            # Update
            optimizer.step()
            scheduler.step()
            optimizer.zero_grad()
            
            total_loss += loss.item()
        
        # Print epoch results
        avg_loss = total_loss / len(dataloader)
        print(f"Epoch {epoch+1}/{config.num_train_epochs} - Avg Loss: {avg_loss:.4f}")
    
    # Save the model
    model_path = os.path.join(output_dir, "vlm_model")
    os.makedirs(model_path, exist_ok=True)
    model.save_pretrained(model_path)
    
    return model

def main():
    args = parse_args()
    
    # Load config
    config = VLMConfig()  # Use default config for now
    
    # Initialize tokenizer and model
    tokenizer = SanskritTokenizer()
    model = VLMCore(config)
    
    # Load data
    dataloader = load_data(args.data_dir, tokenizer, 
                         max_length=config.max_position_embeddings,
                         batch_size=args.batch_size)
    
    # Train model
    model = train(model, dataloader, config, args.output_dir)
    
    print("Training complete!")

if __name__ == "__main__":
    main()
