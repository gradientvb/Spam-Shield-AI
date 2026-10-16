"""
Deep Learning BERT Model Training Module
Fine-tunes DistilBERT for spam detection with comparison to Naive Bayes
"""
import torch
from transformers import (
    DistilBertTokenizer, DistilBertForSequenceClassification,
    Trainer, TrainingArguments, TextClassificationPipeline
)
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, classification_report
import pickle
import warnings

warnings.filterwarnings('ignore')

class SpamDataset(Dataset):
    """Custom PyTorch Dataset for spam detection"""
    
    def __init__(self, texts, labels, tokenizer, max_length=128):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = str(self.texts[idx])
        encoding = self.tokenizer(
            text,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].squeeze(),
            'attention_mask': encoding['attention_mask'].squeeze(),
            'labels': torch.tensor(self.labels[idx], dtype=torch.long)
        }

class BERTSpamDetector:
    """BERT-based Spam Detection Model"""
    
    def __init__(self, model_name='distilbert-base-uncased'):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.tokenizer = DistilBertTokenizer.from_pretrained(model_name)
        self.model = DistilBertForSequenceClassification.from_pretrained(
            model_name,
            num_labels=2
        )
        self.model.to(self.device)
        print(f"📍 Using device: {self.device}")
        print(f"✓ DistilBERT model loaded")
    
    def train(self, X_train, y_train, X_val, y_val, epochs=3, batch_size=32):
        """Train the BERT model"""
        print("\n" + "="*60)
        print("🚀 STARTING BERT MODEL TRAINING")
        print("="*60)
        
        # Create datasets
        train_dataset = SpamDataset(X_train, y_train, self.tokenizer)
        val_dataset = SpamDataset(X_val, y_val, self.tokenizer)
        
        # Training arguments
        training_args = TrainingArguments(
            output_dir='./bert_model',
            num_train_epochs=epochs,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            warmup_steps=100,
            weight_decay=0.01,
            logging_dir='./logs',
            logging_steps=100,
            evaluation_strategy="epoch",
            save_strategy="epoch",
            load_best_model_at_end=True,
            metric_for_best_model="accuracy",
        )
        
        # Trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            compute_metrics=self._compute_metrics,
        )
        
        # Train
        trainer.train()
        print("✓ Training completed!")
        
        return trainer
    
    def _compute_metrics(self, eval_pred):
        """Compute metrics during training"""
        predictions, labels = eval_pred
        predictions = np.argmax(predictions, axis=1)
        
        accuracy = accuracy_score(labels, predictions)
        precision = precision_score(labels, predictions, zero_division=0)
        recall = recall_score(labels, predictions, zero_division=0)
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
        }
    
    def evaluate(self, X_test, y_test, batch_size=32):
        """Evaluate model on test set"""
        print("\n" + "="*60)
        print("📊 EVALUATING BERT MODEL")
        print("="*60)
        
        test_dataset = SpamDataset(X_test, y_test, self.tokenizer)
        test_loader = DataLoader(test_dataset, batch_size=batch_size)
        
        self.model.eval()
        predictions = []
        true_labels = []
        
        with torch.no_grad():
            for batch in test_loader:
                input_ids = batch['input_ids'].to(self.device)
                attention_mask = batch['attention_mask'].to(self.device)
                labels = batch['labels']
                
                outputs = self.model(
                    input_ids=input_ids,
                    attention_mask=attention_mask
                )
                
                logits = outputs.logits
                preds = torch.argmax(logits, dim=1).cpu().numpy()
                
                predictions.extend(preds)
                true_labels.extend(labels.numpy())
        
        # Calculate metrics
        accuracy = accuracy_score(true_labels, predictions)
        precision = precision_score(true_labels, predictions, zero_division=0)
        recall = recall_score(true_labels, predictions, zero_division=0)
        
        print(f"\n📈 Model Metrics:")
        print(f"  Accuracy:  {accuracy:.4f}")
        print(f"  Precision: {precision:.4f}")
        print(f"  Recall:    {recall:.4f}")
        print("\n📋 Classification Report:")
        print(classification_report(true_labels, predictions, 
                                  target_names=['Safe', 'Spam']))
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'predictions': predictions,
            'true_labels': true_labels
        }
    
    def predict(self, text):
        """Single prediction"""
        self.model.eval()
        
        encoding = self.tokenizer(
            text,
            max_length=128,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        
        input_ids = encoding['input_ids'].to(self.device)
        attention_mask = encoding['attention_mask'].to(self.device)
        
        with torch.no_grad():
            outputs = self.model(
                input_ids=input_ids,
                attention_mask=attention_mask
            )
        
        logits = outputs.logits
        probabilities = torch.softmax(logits, dim=1).cpu().numpy()[0]
        prediction = np.argmax(probabilities)
        
        return {
            'is_spam': bool(prediction),
            'safe_probability': float(probabilities[0]),
            'spam_probability': float(probabilities[1])
        }
    
    def save(self, path='models/bert_model'):
        """Save model and tokenizer"""
        self.model.save_pretrained(path)
        self.tokenizer.save_pretrained(path)
        print(f"✓ Model saved to {path}")
    
    def load(self, path='models/bert_model'):
        """Load model and tokenizer"""
        self.model = DistilBertForSequenceClassification.from_pretrained(path)
        self.tokenizer = DistilBertTokenizer.from_pretrained(path)
        self.model = self.model.to(self.device)
        print(f"✓ Model loaded from {path}")

def main():
    """Main training script"""
    print("\n" + "="*70)
    print("  🔬 SPAMSHIELD - BERT vs NAIVE BAYES COMPARISON")
    print("="*70)
    
    # Load data
    print("\n📂 Loading dataset...")
    df = pd.read_csv('dataset/spam.csv', encoding='latin-1')
    df = df[['v1', 'v2']]
    df.columns = ['label', 'message']
    df['label'] = df['label'].map({'ham': 0, 'spam': 1})
    
    print(f"✓ Loaded {len(df)} samples")
    print(f"  Safe messages: {len(df[df['label']==0])}")
    print(f"  Spam messages: {len(df[df['label']==1])}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        df['message'], df['label'],
        test_size=0.2,
        random_state=42,
        stratify=df['label']
    )
    
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train,
        test_size=0.2,
        random_state=42,
        stratify=y_train
    )
    
    print(f"\n📊 Data Split:")
    print(f"  Training:   {len(X_train)} samples")
    print(f"  Validation: {len(X_val)} samples")
    print(f"  Testing:    {len(X_test)} samples")
    
    # Train BERT
    print("\n" + "="*70)
    bert_model = BERTSpamDetector()
    bert_model.train(X_train, y_train, X_val, y_val, epochs=3, batch_size=32)
    
    # Evaluate BERT
    bert_metrics = bert_model.evaluate(X_test, y_test)
    
    # Save BERT
    bert_model.save('models/bert_model')
    
    # Save metrics
    metrics_data = {
        'bert': bert_metrics,
        'timestamp': pd.Timestamp.now()
    }
    
    print("\n" + "="*70)
    print("✅ TRAINING COMPLETE")
    print("="*70)
    print(f"\n🎯 BERT Model Performance:")
    print(f"   Accuracy:  {bert_metrics['accuracy']:.2%}")
    print(f"   Precision: {bert_metrics['precision']:.2%}")
    print(f"   Recall:    {bert_metrics['recall']:.2%}")
    print("\n💾 Models saved to models/ directory")
    print("📊 Ready for production deployment!")

if __name__ == '__main__':
    main()
