import streamlit as st
import pandas as pd

def main():
    st.set_page_config(page_title="Excel Data Viewer", layout="wide")
    st.title("Extract Data from Excel to Streamlit App")

    # File uploader widget
    uploaded_file = st.file_uploader("Upload an Excel file (.xlsx)", type=["xlsx"])

    if uploaded_file is not None:
        try:
            # Read the Excel file into a pandas DataFrame
            df = pd.read_excel(uploaded_file)

            st.success("Excel file loaded successfully!")

            # Display the DataFrame
            st.subheader("Extracted Data:")
            st.dataframe(df)

            # Optional: Display basic statistics
            st.subheader("Data Description:")
            st.write(df.describe())

        except Exception as e:
            st.error(f"Error reading Excel file: {e}")

if __name__ == "__main__":
    main()
