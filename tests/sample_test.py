import pickle

from utils.preprocess import clean_text

# Load model
model = pickle.load(
    open('models/spam_model.pkl', 'rb')
)

# Load vectorizer
vectorizer = pickle.load(
    open('models/vectorizer.pkl', 'rb')
)

# Test messages
test_messages = [

    "URGENT! Claim your FREE prize now",

    "Let's attend class tomorrow",

    "Congratulations! You won cash reward",

    "Please send assignment notes"
]

print("\n========== TEST RESULTS ==========\n")

for msg in test_messages:

    cleaned_message = clean_text(msg)

    vector_input = vectorizer.transform(
        [cleaned_message]
    )

    probability = model.predict_proba(
        vector_input
    )[0][1]

    if probability > 0.40:
        result = "Spam"
    else:
        result = "Safe"

    print(f"Message: {msg}")
    print(f"Prediction: {result}")
    print(f"Spam Probability: {probability * 100:.2f}%")
    print("-" * 50)