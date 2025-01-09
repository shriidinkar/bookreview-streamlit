import streamlit as st
import requests

# Streamlit app title
st.title("📚 Book Search")

# Input box for book search
book_name = st.text_input("Enter book name to search:", "")

# Function to get book description from the works endpoint
@st.cache_data
def get_book_description(work_id):
    try:
        url = f"https://openlibrary.org/works/{work_id}.json"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get("description", {}).get("value", "Description not available") if isinstance(data.get("description"), dict) else data.get("description", "Description not available")
        else:
            return "Description not available"
    except:
        return "Description not available"

# Function to generate book cover image URL
def get_cover_image_url(cover_id):
    if cover_id:
        return f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
    return "https://via.placeholder.com/150?text=No+Image"

# Check if user entered a book name
if book_name:
    with st.spinner("Searching for books..."):
        # Open Library API URL
        api_url = f"https://openlibrary.org/search.json?q={book_name}"
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            if data["docs"]:
                for book in data["docs"][:5]:
                 # Display cover image
                    cover_id = book.get("cover_i")
                    cover_image_url = get_cover_image_url(cover_id)
                    st.image(cover_image_url, caption="Cover Image", use_container_width=True)

                    # Display book details
                    st.subheader(f"📖 {book.get('title', 'N/A')}")
                    st.write("**Author(s):**", ", ".join(book.get("author_name", ["N/A"])))
                    st.write("**First Published Year:**", book.get("first_publish_year", "N/A"))
                    
                    # Get the work ID and fetch the description
                    work_id = book.get("key", "").split("/")[-1]
                    description = get_book_description(work_id)
                    st.write("**Description:**", description)

                    st.write("---")
            else:
                st.warning("No books found.")
        else:
            st.error(f"Error: Unable to fetch data (Status code: {response.status_code})")
