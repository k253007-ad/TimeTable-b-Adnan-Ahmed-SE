import streamlit as st
import pandas as pd

st.set_page_config(page_title="Timetable Splitter", layout="wide")

st.title("📅 Timetable Splitter by Class")

# File uploader
uploaded_file = st.file_uploader("Upload your timetable Excel file", type=["xlsx"])

if uploaded_file:
    # Read Excel file
    df = pd.read_excel(uploaded_file)

    st.subheader("Raw Timetable Data Preview")
    st.dataframe(df.head())

    # Ask which column identifies classes
    class_column = st.selectbox("Select the column that represents classes", df.columns)

    if class_column:
        classes = df[class_column].unique()
        st.write(f"Found {len(classes)} unique classes")

        # Show timetable per class
        selected_class = st.selectbox("Select a class to view its timetable", classes)

        class_df = df[df[class_column] == selected_class]
        st.subheader(f"Timetable for class: {selected_class}")
        st.dataframe(class_df)

        # Option to download class timetable
        def convert_df_to_excel(dataframe):
            from io import BytesIO
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                dataframe.to_excel(writer, index=False, sheet_name="Timetable")
            processed_data = output.getvalue()
            return processed_data

        excel_data = convert_df_to_excel(class_df)
        st.download_button(
            label=f"Download timetable for {selected_class}",
            data=excel_data,
            file_name=f"{selected_class}_timetable.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # Option to download all classes separately in one zip
        import zipfile, io

        if st.button("Download all classes as ZIP"):
            buffer = io.BytesIO()
            with zipfile.ZipFile(buffer, "w") as zf:
                for cls in classes:
                    cls_df = df[df[class_column] == cls]
                    excel_bytes = convert_df_to_excel(cls_df)
                    zf.writestr(f"{cls}_timetable.xlsx", excel_bytes)
            buffer.seek(0)
            st.download_button(
                label="Download ZIP of all classes",
                data=buffer,
                file_name="all_classes_timetables.zip",
                mime="application/zip"
            )
