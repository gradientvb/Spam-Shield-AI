from flask import Flask, render_template, request
import pickle

from utils.preprocess import clean_text
from utils.helper import detect_keywords

# Initialize Flask App
app = Flask(__name__)

# Load trained model
model = pickle.load(
    open('models/spam_model.pkl', 'rb')
)

# Load TF-IDF vectorizer
vectorizer = pickle.load(
    open('models/vectorizer.pkl', 'rb')
)


# Home Route
@app.route('/')
def home():

    return render_template('index.html')


# Prediction Route
@app.route('/predict', methods=['POST'])
def predict():

    # Get message from form
    message = request.form['message']

    # Clean message
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

    # Detect suspicious keywords
    keywords = detect_keywords(message)

    # Final prediction
    if spam_probability > 0.40:
        result = "Spam Message"
    else:
        result = "Safe Message"

    # Render output
    return render_template(

        'index.html',

        prediction=result,

        probability=round(
            spam_probability * 100,
            2
        ),

        keywords=keywords
    )


# Run Flask App
if __name__ == '__main__':

    app.run(debug=True)