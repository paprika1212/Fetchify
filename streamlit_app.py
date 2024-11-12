import time
import streamlit as st
from components.sidebar import sidebar
import pandas as pd
from components.streamresults import stream_data

st.set_page_config(page_title="Fetchify", page_icon="🔎", layout="wide")
st.header("Fetchify 🔎")

sidebar()

openai_api_key = st.session_state.get("OPENAI_API_KEY")
if not openai_api_key:
    st.warning(
        "Enter your OpenAI API key in the sidebar. You can get a key at"
        " https://platform.openai.com/account/api-keys."
    )




def long_running_function():
    time.sleep(5)  # Simulate a delay
    # Example result: could be replaced with actual data processing results
    result_data = pd.DataFrame({
        "Entity": ["Company A", "Company B", "Company C"],
        "Email": ["a@example.com", "b@example.com", "c@example.com"],
    })
    return result_data






uploaded_file = st.file_uploader("Upload a CSV file", accept_multiple_files=False)
if uploaded_file is not None:
    try:
        # Attempt to load and display the CSV file
        df = pd.read_csv(uploaded_file)
        st.write("### Full Dataset")
        
        # Display the dataframe
        st.dataframe(df, use_container_width=True, height=400)
        
        # Selecting column for filtering
        columns = df.columns.tolist()
        selected_column = st.selectbox("Select column to filter by", columns)
        
        # Displaying unique entries from the selected column
        filtered_df = df[selected_column]
        unique_values = df[selected_column].unique()
        st.write("Filtered Column:", filtered_df)
        
        st.text_input(
            "Input your search query for each entry in the column, using placeholders :  ",
            "Eg : ",
            key="query"
        )

        if st.button("Start Fetching Data"):
            with st.spinner("Fetching data, please wait..."):
             # Run the long-running function and store results
                results = long_running_function()

            st.success("Results fetched successfully!")

    
            if st.button("Show Results"):
                # Display the results
                st.write("Here are your results:")
                st.stream_data(results)

        st.button("Rerun")

    except pd.errors.EmptyDataError:
        st.error("The uploaded file is empty. Please upload a valid CSV file.")
    except pd.errors.ParserError:
        st.error("Error parsing CSV file. Ensure the file is formatted correctly.")
    except KeyError as e:
        st.error(f"Column selection error: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")