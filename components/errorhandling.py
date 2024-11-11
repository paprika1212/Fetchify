import pandas as pd
import streamlit as st
import logging
import traceback

# Configure logging
logging.basicConfig(filename="fetchify_errors.log", level=logging.ERROR)

def handle_error(error, context=""):
    """
    Handles errors in a Streamlit application, logs the error, and displays it to the user.
    
    Parameters:
        error (Exception): The error instance to handle.
        context (str): A string providing context on where the error occurred.
    """
    error_type = type(error).__name__
    error_message = str(error)
    detailed_traceback = traceback.format_exc()

    # Log the error for internal analysis
    logging.error(f"Context: {context}\nError Type: {error_type}\nMessage: {error_message}\nTraceback:\n{detailed_traceback}")

    # Display error messages to the user based on the context
    if context == "file_upload":
        st.error("There was an error with the file upload. Please ensure the file format is correct and try again.")
    elif context == "google_sheet_connection":
        st.error("Unable to connect to Google Sheets. Please check your credentials or internet connection.")
    elif context == "web_search":
        st.warning("An error occurred while performing the web search. This might be due to API rate limits or network issues. Please try again later.")
    elif context == "llm_processing":
        st.warning("There was an error with LLM processing. Please ensure the prompt format is correct, and try again.")
    elif context == "data_display":
        st.error("An error occurred while displaying the data. Please refresh or try again.")
    else:
        st.error("An unexpected error occurred. Please try again or contact support if the issue persists.")
        
    # Show detailed error information to advanced users
    with st.expander("Show detailed error info"):
        st.text(f"Error Type: {error_type}")
        st.text(f"Error Message: {error_message}")
        st.text(detailed_traceback)

# Example usage in Fetchify app
def fetchify_dashboard():
    st.title("Fetchify - AI Data Fetching and Extraction")

    try:
        # File upload section
        file = st.file_uploader("Upload a CSV file")
        if file:
            try:
                data = pd.read_csv(file)
                st.write("File uploaded successfully!")
                st.dataframe(data.head())
            except Exception as e:
                handle_error(e, context="file_upload")

        # Google Sheets connection
        google_sheet_url = st.text_input("Enter Google Sheet URL (optional)")
        if google_sheet_url:
            try:
                # Assume connect_to_google_sheet is a function that fetches data from Google Sheets
                data = connect_to_google_sheet(google_sheet_url)
                st.write("Google Sheets data loaded successfully!")
                st.dataframe(data.head())
            except Exception as e:
                handle_error(e, context="google_sheet_connection")

        # LLM processing section
        user_query = st.text_input("Define your query using placeholders (e.g., 'Get me the email address of {company}')")
        if st.button("Fetch Data"):
            try:
                if not user_query:
                    raise ValueError("Query cannot be empty. Please provide a valid query.")
                
                # Assume run_llm_query is a function that uses the LLM to process the data
                results = run_llm_query(data, user_query)
                st.write("Data fetched successfully!")
                st.dataframe(results)
            except Exception as e:
                handle_error(e, context="llm_processing")

    except Exception as e:
        handle_error(e)

# Define other utility functions
def connect_to_google_sheet(sheet_url):
    """ Placeholder function to simulate Google Sheets data retrieval. """
    # Your connection and data retrieval logic here
    pass

def run_llm_query(data, query):
    """ Placeholder function to simulate LLM data processing. """
    # Your LLM integration and processing logic here
    pass

# Run the dashboard
fetchify_dashboard()
