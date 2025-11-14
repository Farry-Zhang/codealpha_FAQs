import streamlit as st
import nltk
import string
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 下载 NLTK 数据（第一次运行需要）
nltk.download('punkt')
nltk.download('stopwords')

# FAQ 数据
faqs = [
    {"question": "What is your return policy?",
     "answer": "You can return any item within 30 days for a full refund."},
    {"question": "How can I track my order?",
     "answer": "You can track your order using the tracking link sent to your email."},
    {"question": "Do you offer international shipping?",
     "answer": "Yes, we ship to over 50 countries worldwide."},
    {"question": "What payment methods do you accept?",
     "answer": "We accept Visa, MasterCard, PayPal, and Apple Pay."},
    {"question": "How can I contact customer service?",
     "answer": "You can reach us via the contact form or call 1-800-555-1234."}
]

# 文本预处理
def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = nltk.word_tokenize(text)
    tokens = [t for t in tokens if t not in stopwords.words('english')]
    return " ".join(tokens)

# 预处理 FAQ 问题
faq_questions = [preprocess(f["question"]) for f in faqs]
vectorizer = TfidfVectorizer()
faq_vectors = vectorizer.fit_transform(faq_questions)

# 匹配函数
def get_answer(user_input):
    user_input_clean = preprocess(user_input)
    user_vec = vectorizer.transform([user_input_clean])
    similarities = cosine_similarity(user_vec, faq_vectors)
    best_match_idx = similarities.argmax()
    best_score = similarities[0, best_match_idx]
    if best_score < 0.2:
        return "Sorry, I’m not sure about that. Could you rephrase your question?"
    else:
        return faqs[best_match_idx]["answer"]

# Streamlit UI
st.title("FAQ Chatbot")
st.write("Ask me anything about our store!")

user_input = st.text_input("You:")

if user_input:
    answer = get_answer(user_input)
    st.text_area("Chatbot:", value=answer, height=100)
