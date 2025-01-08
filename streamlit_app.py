import streamlit as st
import requests

# Streamlit app
st.title("📚 Google Books Search")

# Input box for book search
book_name = st.text_input("Enter book name to search:", "")

# Check if user entered a book name
if book_name:
    # Google Books API URL
    api_url = f"https://www.googleapis.com/books/v1/volumes?q={book_name}"

    # Send request to the API
    response = requests.get(api_url)

    # Check if request was successful
    if response.status_code == 200:
        data = response.json()

        # Check if any books were found
        if "items" in data:
            # Display details of the first 5 books
            for book in data["items"][:5]:
                volume_info = book["volumeInfo"]
                st.subheader(f"📖 Book Title: {volume_info.get('title', 'N/A')}")
                st.warning(f"**Author(s):** {', '.join(volume_info.get('authors', ['N/A']))}")
                st.write("**Publisher:**", volume_info.get("publisher", "N/A"))
                st.write("**Published Date:**", volume_info.get("publishedDate", "N/A"))
                st.info(f"Description: {volume_info.get('description', 'N/A')}")
                st.write("---")
        else:
            st.write("No books found.")
    else:
        st.error("Failed to fetch data from Google Books API.")
