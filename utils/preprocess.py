import re
import string
import nltk

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# Download stopwords
nltk.download('stopwords')

# Stemmer
ps = PorterStemmer()

# Custom stopwords
custom_stopwords = stopwords.words('english')

# Important spam words that should NOT be removed
important_words = [
    'not',
    'no',
    'free',
    'won',
    'winner',
    'cash',
    'prize',
    'claim',
    'urgent',
    'offer'
]

# Remove important words from stopwords list
custom_stopwords = [
    word for word in custom_stopwords
    if word not in important_words
]


def clean_text(text):

    # Convert to lowercase
    text = text.lower()

    # Remove numbers
    text = re.sub(r'\d+', '', text)

    # Remove punctuation
    text = text.translate(
        str.maketrans('', '', string.punctuation)
    )

    # Split text into words
    words = text.split()

    cleaned_words = []

    for word in words:

        # Remove stopwords
        if word not in custom_stopwords:

            # Apply stemming
            stemmed_word = ps.stem(word)

            cleaned_words.append(stemmed_word)

    # Join words back into sentence
    return " ".join(cleaned_words)