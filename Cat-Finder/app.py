import streamlit as st
import requests

st.set_page_config(
    page_title="Random Cat Finder",
    page_icon="🐱"
)

st.title("🐱 Random Cat Finder")

st.write("Discover a cute random cat with just one click!")

if st.button("🐱 Get Another Cat"):

    try:
        response = requests.get(
            "https://api.thecatapi.com/v1/images/search"
        )

        response.raise_for_status()

        data = response.json()

        cat_url = data[0]["url"]

        st.image(
            cat_url,
            caption="Here is your random cat! 🐱",
            use_container_width=True
        )

    except Exception:
        st.error("Oops! Something went wrong. Please try again.")