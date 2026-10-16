import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report
)

from utils.preprocess import clean_text

# Load Dataset
df = pd.read_csv(
    'dataset/spam.csv',
    encoding='latin-1'
)

# Keep required columns only
df = df[['v1', 'v2']]

# Rename columns
df.columns = ['label', 'message']

# Convert labels into numbers
df['label'] = df['label'].map({
    'ham': 0,
    'spam': 1
})

# Clean messages
df['message'] = df['message'].apply(
    clean_text
)

# Features and labels
X = df['message']
y = df['label']

# TF-IDF Vectorization
vectorizer = TfidfVectorizer(
    max_features=3000,
    ngram_range=(1, 2)
)

X = vectorizer.fit_transform(X)

# Split Dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train Model
model = MultinomialNB()

model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(
    y_test,
    y_pred
)

print(f"\nAccuracy: {accuracy * 100:.2f}%")

# Confusion Matrix
cm = confusion_matrix(
    y_test,
    y_pred
)

print("\nConfusion Matrix:\n")
print(cm)

# Classification Report
report = classification_report(
    y_test,
    y_pred
)

print("\nClassification Report:\n")
print(report)

# Save Model
pickle.dump(
    model,
    open('models/spam_model.pkl', 'wb')
)

# Save Vectorizer
pickle.dump(
    vectorizer,
    open('models/vectorizer.pkl', 'wb')
)

print("\nModel Saved Successfully")