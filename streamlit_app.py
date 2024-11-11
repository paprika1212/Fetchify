import streamlit as st
from components.sidebar import sidebar
import pandas as pd

st.set_page_config(page_title="Fetchify", page_icon="🔎", layout="wide")
st.header("Fetchify 🔎")

sidebar()

openai_api_key = st.session_state.get("OPENAI_API_KEY")
if not openai_api_key:
    st.warning(
        "Enter your OpenAI API key in the sidebar. You can get a key at"
        " https://platform.openai.com/account/api-keys."
    )

uploaded_file = st.file_uploader("Upload a CSV file", accept_multiple_files=False)
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.write("### Full Dataset")
        
        selection = st.dataframe(
                df,
                key="interactive_df",
                on_select="rerun",
                use_container_width=True,
                height=400,
                selection_mode="single-column"
            )
        


        columns = df.columns.tolist()
        selected_column = st.selectbox("Select column to filter by", columns)

        filtered_df = df[selected_column]
        unique_values = df[selected_column].unique()
        entries = df.iloc[:, [selected_column]]
        st.write(filtered_df)

    except:
        st.write("error")
