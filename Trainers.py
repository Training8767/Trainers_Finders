import streamlit as st
from serpapi import GoogleSearch
import pandas as pd

# Set colorful page config
st.set_page_config(
    page_title="🎨 Crazy Colorful Trainer Finder",
    layout="centered",
    page_icon="🎯"
)

# Inject custom CSS for wild styling
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
        color: #000000;
    }
    .stTextInput > div > div > input {
        background-color: #fffbe6;
        color: #000000;
    }
    .stButton>button {
        background-color: #ff4b1f;
        color: white;
        font-weight: bold;
        border-radius: 12px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1fddff;
        color: black;
    }
    .stDataFrame {
        background-color: #ffffffaa;
    }
    .css-18e3th9 {
        padding: 3rem 1rem;
        border-radius: 10px;
        background-color: rgba(255, 255, 255, 0.8);
    }
    </style>
""", unsafe_allow_html=True)

# Title with Emojis
st.title("🌈💼 Trainer Finder Tool using SerpAPI 🎯")
st.subheader("Find professional trainers from LinkedIn using Google Search via SerpAPI")

st.markdown("### ✨ Enter Search Details Below")

# Input form
with st.form("search_form"):
    domain = st.text_input("📘 Enter Domain (e.g., Python, Java)", "")
    location = st.text_input("📍 Enter Location (e.g., Pune)", "")
    keyword = st.text_input("🧩 Optional Keywords (e.g., freelance, corporate)", "")
    serpapi_key = st.text_input("🔑 Enter your SerpAPI Key", type="password")
    submitted = st.form_submit_button("🚀 Search Trainers")

if submitted:
    if not domain or not location or not serpapi_key:
        st.error("❗ Please enter all required fields including SerpAPI key.")
    else:
        with st.spinner("🔍 Searching trainers using SerpAPI..."):
            query = f'site:linkedin.com/in/ "{domain} trainer" AND "{location}" {keyword}'

            params = {
                "engine": "google",
                "q": query,
                "api_key": serpapi_key,
                "num": "50"
            }

            try:
                search = GoogleSearch(params)
                results = search.get_dict()

                profiles = []
                if "organic_results" in results:
                    for res in results["organic_results"]:
                        link = res.get("link", "")
                        title = res.get("title", "")
                        snippet = res.get("snippet", "")
                        if "linkedin.com/in/" in link:
                            profiles.append({
                                "Name/Title": title,
                                "Snippet": snippet,
                                "LinkedIn URL": link
                            })

                if profiles:
                    df = pd.DataFrame(profiles).drop_duplicates(subset=["LinkedIn URL"])
                    st.balloons()
                    st.success(f"🎉 Found {len(df)} trainer profiles!")
                    st.dataframe(df, use_container_width=True)

                    csv = df.to_csv(index=False).encode("utf-8")
                    st.download_button("⬇️ Download CSV", data=csv, file_name="trainers.csv", mime="text/csv")
                else:
                    st.warning("😕 No trainer profiles found. Try changing keywords or location.")
            except Exception as e:
                st.error(f"💥 Something went wrong: {e}")
