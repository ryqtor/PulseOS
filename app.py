import streamlit as st
from textblob import TextBlob
import base64
import os

st.set_page_config(page_title="PulseOS", layout="wide")

def load_logo_b64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

logo_b64 = load_logo_b64("pulseos_logo.png")

header_html = (
    '<div style="display:flex; align-items:center; justify-content:center; gap:14px; margin-top:20px;">'
    f'<img src="data:image/png;base64,{logo_b64}" style="height:60px;">'
    '<div>'
    '<h1 style="margin:0; font-size:28px; font-weight:700;">'
    '- Product Review Sentiment Analyzer'
    '</h1>'
    '<p style="margin:0; text-align:center; color:#555;">'
    'Analyze smartwatch reviews in real time using TextBlob polarity'
    '</p>'
    '</div>'
    '</div>'
)

st.markdown(header_html, unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

if "sentiment" not in st.session_state:
    st.session_state["sentiment"] = None

st.subheader("Enter a smartwatch review")
st.text_area(
    "Product Review",
    key="review_input",
    height=150,
    placeholder="Type your review here..."
)

NEGATION_WORDS = {"not", "no", "never", "n't", "cannot", "can't", "don't", "didn't", "won't", "couldn't", "shouldn't", "hardly", "barely"}

def do_clear():
    st.session_state["review_input"] = ""
    st.session_state["sentiment"] = None

def do_analyze():
    text = st.session_state.get("review_input", "").strip()
    if not text:
        st.session_state["sentiment"] = "__EMPTY__"
        return

    txt = " ".join(text.split()).lower()
    polarity = TextBlob(txt).sentiment.polarity

    if any(n in txt for n in NEGATION_WORDS):
        polarity -= 0.35

    POS_THRESHOLD = 0.25
    NEG_THRESHOLD = -0.25

    if polarity > POS_THRESHOLD:
        st.session_state["sentiment"] = "Positive"
    elif polarity < NEG_THRESHOLD:
        st.session_state["sentiment"] = "Negative"
    else:
        st.session_state["sentiment"] = "Neutral"

col1, col2 = st.columns([1, 1])
with col1:
    st.button("Analyze Sentiment", on_click=do_analyze)
with col2:
    st.button("Clear Text", on_click=do_clear)

s = st.session_state.get("sentiment", None)

if s == "__EMPTY__":
    st.warning("Please enter a review to analyze.")
elif s in ("Positive", "Negative", "Neutral"):
    if s == "Positive":
        bg = "#A5D6A7"
        color = "#1B5E20"
    elif s == "Negative":
        bg = "#EF9A9A"
        color = "#B71C1C"
    else:
        bg = "#E0E0E0"
        color = "#424242"

    result_html = (
        '<div style="text-align:center; margin-top:20px;">'
        '<div style="font-size:20px; font-weight:700; margin-bottom:10px;">Analyzed Sentiment</div>'
        f'<span style="font-size:22px; font-weight:800; background:{bg}; color:{color}; padding:6px 16px; border-radius:6px;">'
        f'{s}'
        '</span>'
        '</div>'
    )
    st.markdown(result_html, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)