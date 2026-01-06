import streamlit as st
from scrape import scrape_website

st.set_page_config(page_title="Universal Web Scraper", layout="centered")
st.title("🌐 Universal Web Scraper")

st.write("Scrapes visible text from a website (main page + few internal pages).")

# Initialize session state
if "lines" not in st.session_state:
    st.session_state.lines = []

url = st.text_input("Enter website URL", placeholder="https://example.com")

max_pages = st.slider(
    "How many pages to scrape?",
    min_value=1,
    max_value=5,
    value=3
)

# Scrape button
if st.button("Scrape Website"):
    if not url:
        st.warning("Please enter a website URL.")
    else:
        with st.spinner("Scraping website..."):
            try:
                st.session_state.lines = scrape_website(url, max_pages=max_pages)
                st.success(
                    f"Scraped {len(st.session_state.lines)} lines from {max_pages} page(s)."
                )
            except Exception as e:
                st.error(f"Error occurred: {e}")
                st.session_state.lines = []

# Show results only if data exists
if st.session_state.lines:
    keyword = st.text_input(
        "Filter by keyword (optional)",
        placeholder="example: price, contact, course"
    )

    filtered_lines = st.session_state.lines

    if keyword:
        filtered_lines = [
            l for l in st.session_state.lines
            if keyword.lower() in l.lower()
        ]

    st.text_area(
        "Extracted Text",
        "\n".join(filtered_lines),
        height=400
    )
