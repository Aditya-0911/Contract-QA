import streamlit as st
from ui import show_main_page

def main():
    st.set_page_config(page_title="Contract Analyzer", page_icon="📄", layout="wide")
    show_main_page()

if __name__ == "__main__":
    main()
