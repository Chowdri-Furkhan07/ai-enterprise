import streamlit as st
import requests

st.title("Enterprise AI Assistant")

role = st.selectbox("Role", ["admin", "analyst", "viewer"])
file = st.file_uploader("Upload file")

if file:
    requests.post("http://localhost:8000/upload", files={"file": file})

query = st.text_input("Ask")

if st.button("Submit"):
    res = requests.post(
        "http://localhost:8000/query",
        params={"q": query, "role": role}
    )
    st.write(res.json()["response"])