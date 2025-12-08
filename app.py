import streamlit as st
import pandas as pd
import json
import os

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from utils.data_manager import (
    load_books, save_books, ensure_data_directory, commit_to_github
)
from config.settings import (
    APP_TITLE, MAX_VOTES_PER_PERSON, TOTAL_POINTS, TOP_BOOKS_TO_DISPLAY
)

# ==================== APP CONFIG ====================
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .book-container {
        padding: 1rem;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== DATA LOADING ====================
if "books" not in st.session_state:
    st.session_state.books = load_books()

def auto_save():
    save_books(st.session_state.books)

# ==================== VIEW BOOKS ====================
st.markdown('<p class="main-header">📖 Get to know the submitted books!</p>',
            unsafe_allow_html=True)

if not st.session_state.books:
    st.warning("📚 No books have been submitted yet. Please go to 'Submit Books' page first.")

else:
    st.header("📚 Submitted Books")

    # Sort by last name of author safely
    def author_last_name(book):
        parts = book["author"].split()
        return parts[-1] if parts else ""

    sorted_books = sorted(st.session_state.books, key=author_last_name)

    for idx, book in enumerate(sorted_books):
        with st.container():
            col1, col2 = st.columns([1, 3])

            # -------- COVER COLUMN --------
            with col1:
                clean_title = book["title"].replace(" ", "_").replace(":", "").replace("?", "")
                cover_path = f"covers/{clean_title}.jpg"

                if os.path.exists(cover_path):
                    st.image(cover_path, use_container_width=True)
                else:
                    st.markdown(f"""
                        <div style="
                            background-color: white;
                            border: 1px solid #ddd;
                            padding: 40px 20px;
                            text-align: center;
                            min-height: 400px;
                            display: flex;
                            flex-direction: column;
                            justify-content: center;
                        ">
                            <p style="color: black; font-size: 1.2rem; font-weight: bold; margin-bottom: 10px;">
                                {book['title']}
                            </p>
                            <p style="color: #666; font-size: 1rem;">
                                {book['author']}
                            </p>
                        </div>
                    """, unsafe_allow_html=True)

            # -------- DETAILS COLUMN --------
            with col2:
                st.subheader(book["title"])
                st.write(f"**Author:** {book['author']}")
                st.write(f"**Year:** {book.get('year', 'N/A')}")
                st.write(f"**Genre:** {book.get('genres', 'N/A')}")
                st.write(f"**Pages:** {book.get('pages', 'N/A')}")
                st.write(f"**Link:** {book.get('url', 'N/A')}")
                st.write(f"**Summary:** {book.get('summary', 'No summary available')}")

            st.divider()
