# Suspicious spam keywords

spam_keywords = [

    'free',
    'winner',
    'won',
    'cash',
    'prize',
    'offer',
    'urgent',
    'click',
    'money',
    'lottery',
    'reward',
    'claim',
    'congratulations',
    'buy now',
    'limited',
    'selected'
]


def detect_keywords(message):

    detected_words = []

    message = message.lower()

    for word in spam_keywords:

        if word.lower() in message:
            detected_words.append(word)

    return list(set(detected_words))