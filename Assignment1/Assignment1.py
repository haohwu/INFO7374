import streamlit as st
import json
import nltk
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')

def extract_keywords(query):
    words = nltk.word_tokenize(query)
    filtered_words = [word for word in words if word not in stopwords.words('english')]
    return filtered_words

intents = {
    'menus': ['menu', 'food', 'dishes', 'eat'],
    'about': ['about', 'info', 'information', 'history'],
    'hours': ['hours', 'time', 'open', 'close'],
    'events': ['events', 'weddings', 'parties', 'bookings'],
    'employment': ['jobs', 'career', 'hiring', 'employment'],
    'reservations': ['reserve', 'booking', 'reservation', 'book']
}


def classify_intent(query):
    query = query.lower().split()
    for intent, keywords in intents.items():
        if any(keyword in query for keyword in keywords):
            return intent
    return 'unknown' 


# Load data
def load_data():
    with open('data.json', 'r') as file:
        return json.load(file)

data = load_data()

# Function to process input and generate response
def get_response(query, data):
    # Assume a function 'classify_intent' and 'extract_keywords' are implemented
    intent = classify_intent(query)
    keywords = extract_keywords(query)
    if intent in data:
        return data[intent]  # Simplified response logic
    return "I'm not sure how to answer that, could you ask differently?"

st.title('Toro Restaurant Chatbot')
query = st.text_input("Ask me anything about Toro Restaurant:")
if query:
    response = get_response(query, data)
    st.write(response)
