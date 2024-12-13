import streamlit as st
from scrape1 import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
)
from parse import parse_with_ollama
import datetime

# Initial values
# weburl = "http://olympics.com/en/paris-2024/medals"
# prompt = """
#     can you please give a table that contains all the countries that received atleast one gold medal 
#     in the 2024 olympics and show me the country name and medal count. Please respond with a nicely formatted 
#     table that is easy to read. Please do not include any additional text, comments, or explanations in your response. 
#     Only give the table. Do not include any other text. """

# weburl = "https://www.linkedin.com/in/sankarvema/"
# prompt = """can you please give me a json that contains all the details of the linkedin profile of sankarvema"""

# weburl = "https://www.linkedin.com/mynetwork/invite-connect/connections/"
weburl = "https://www.linkedin.com/search/results/people/?facetConnectionOf=%5B%22ACoAAACxz8oB9KMGAuE26mUwRE7GYLJaVrYGPLA%22%5D&facetNetwork=%5B%22F%22%5D&origin=SHARED_CONNECTIONS_CANNED_SEARCH&sid=)cQ"
prompt = """parsing the content of the linkedin network of sankarvema, please give me a json that 
contains total count of connections and an arry containing each connection information like name, designation, 
contact info, current company"""

# Streamlit UI
st.title("AI Web Scraper")
url = st.text_input("Enter Website URL", weburl)

# Step 1: Scrape the Website
if st.button("Scrape Website"):
    if url:
        st.write("Scraping the website...")

        # Scrape the website
        dom_content = scrape_website(url)
        body_content = extract_body_content(dom_content)
        cleaned_content = clean_body_content(body_content)

        # Store the DOM content in Streamlit session state
        st.session_state.dom_content = cleaned_content

        # Display the DOM content in an expandable text box
        with st.expander("View DOM Content"):
            st.text_area("DOM Content", cleaned_content, height=300)


# Step 2: Ask Questions About the DOM Content
if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse", prompt)

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content...")

            # Parse the content with Ollama
            dom_chunks = split_dom_content(st.session_state.dom_content)
            parsed_result = parse_with_ollama(dom_chunks, parse_description)
            st.write(parsed_result)

            f = open("output.txt", "a")
            f.write("\n" + "-"*25 + "\n")
            f.write(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n")
            f.write(url + "\n")
            f.write(prompt + "\n")
            f.write("\n" + "-"*25 + "\n")

            f.write(parsed_result)
            f.close()
