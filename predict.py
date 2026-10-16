import pickle

from utils.preprocess import clean_text

# Load trained model
model = pickle.load(
    open('models/spam_model.pkl', 'rb')
)

# Load vectorizer
vectorizer = pickle.load(
    open('models/vectorizer.pkl', 'rb')
)

# User input
message = input("Enter Message: ")

# Clean text
cleaned_message = clean_text(message)

# Convert text into vector
vector_input = vectorizer.transform(
    [cleaned_message]
)

# Get prediction probability
prediction_proba = model.predict_proba(
    vector_input
)[0]

# Spam probability
spam_probability = prediction_proba[1]

# Print probability
print(f"\nSpam Probability: {spam_probability * 100:.2f}%")

# Custom threshold
if spam_probability > 0.40:
    print("\nSpam Message")
else:
    print("\nNot Spam")