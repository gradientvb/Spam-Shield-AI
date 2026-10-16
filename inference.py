"""
BERT Inference Module - Real-time predictions using trained BERT model
Provides unified interface for both Naive Bayes and BERT predictions
"""
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import pickle
import numpy as np
from utils.preprocess import clean_text
from utils.helper import detect_keywords

class UnifiedSpamDetector:
    """Unified interface for both Naive Bayes and BERT models"""
    
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.nb_model = None
        self.nb_vectorizer = None
        self.bert_model = None
        self.bert_tokenizer = None
        self.load_models()
    
    def load_models(self):
        """Load both models"""
        try:
            self.nb_model = pickle.load(open('models/spam_model.pkl', 'rb'))
            self.nb_vectorizer = pickle.load(open('models/vectorizer.pkl', 'rb'))
            print("✓ Naive Bayes model loaded")
        except Exception as e:
            print(f"⚠ Naive Bayes model not available: {e}")
        
        try:
            self.bert_tokenizer = DistilBertTokenizer.from_pretrained('models/bert_model')
            self.bert_model = DistilBertForSequenceClassification.from_pretrained('models/bert_model')
            self.bert_model.to(self.device)
            print("✓ BERT model loaded")
        except Exception as e:
            print(f"⚠ BERT model not available: {e}")
    
    def predict_naive_bayes(self, text):
        """Predict using Naive Bayes"""
        if not self.nb_model:
            return None
        
        cleaned_text = clean_text(text)
        vector_input = self.nb_vectorizer.transform([cleaned_text])
        prediction_proba = self.nb_model.predict_proba(vector_input)[0]
        
        return {
            'is_spam': bool(prediction_proba[1] > 0.40),
            'safe_probability': float(prediction_proba[0]),
            'spam_probability': float(prediction_proba[1]),
            'model': 'naive_bayes'
        }
    
    def predict_bert(self, text):
        """Predict using BERT"""
        if not self.bert_model:
            return None
        
        self.bert_model.eval()
        
        encoding = self.bert_tokenizer(
            text,
            max_length=128,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        
        input_ids = encoding['input_ids'].to(self.device)
        attention_mask = encoding['attention_mask'].to(self.device)
        
        with torch.no_grad():
            outputs = self.bert_model(
                input_ids=input_ids,
                attention_mask=attention_mask
            )
        
        logits = outputs.logits
        probabilities = torch.softmax(logits, dim=1).cpu().numpy()[0]
        prediction = np.argmax(probabilities)
        
        return {
            'is_spam': bool(prediction),
            'safe_probability': float(probabilities[0]),
            'spam_probability': float(probabilities[1]),
            'model': 'bert'
        }
    
    def ensemble_predict(self, text, weights={'bert': 0.6, 'nb': 0.4}):
        """
        Ensemble prediction combining both models
        Default: 60% BERT + 40% Naive Bayes
        """
        bert_result = self.predict_bert(text)
        nb_result = self.predict_naive_bayes(text)
        
        # Ensemble voting
        if bert_result and nb_result:
            ensemble_spam_prob = (
                bert_result['spam_probability'] * weights['bert'] +
                nb_result['spam_probability'] * weights['nb']
            )
            
            return {
                'is_spam': ensemble_spam_prob > 0.40,
                'ensemble_spam_probability': float(ensemble_spam_prob),
                'bert_spam_probability': bert_result['spam_probability'],
                'naive_bayes_spam_probability': nb_result['spam_probability'],
                'model': 'ensemble',
                'confidence': max(ensemble_spam_prob, 1 - ensemble_spam_prob)
            }
        elif bert_result:
            return bert_result
        elif nb_result:
            return nb_result
        else:
            raise RuntimeError("No models loaded")
    
    def predict_with_explanation(self, text, model_type='ensemble'):
        """Predict with explainability - returns keywords and confidence"""
        
        if model_type == 'bert':
            result = self.predict_bert(text)
        elif model_type == 'naive_bayes':
            result = self.predict_naive_bayes(text)
        else:
            result = self.ensemble_predict(text)
        
        # Add keywords
        keywords = detect_keywords(text)
        
        return {
            **result,
            'detected_keywords': keywords,
            'prediction': '🚨 SPAM' if result['is_spam'] else '✅ SAFE'
        }

# Global detector instance
detector = None

def get_detector():
    """Get or create global detector instance"""
    global detector
    if detector is None:
        detector = UnifiedSpamDetector()
    return detector

def predict(text, model_type='ensemble'):
    """Convenience function for predictions"""
    return get_detector().predict_with_explanation(text, model_type)
