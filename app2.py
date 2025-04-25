import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Data Statistics App", layout="centered")

st.title("📊 Data Statistics Web App")

# Step 1: Upload Excel File
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file:
    # Step 2: Read Excel file
    df = pd.read_excel(uploaded_file)
    st.subheader("📂 Preview of Uploaded Data")
    st.dataframe(df)

    # Step 3: Column selection
    column_name = st.selectbox("Select a column to analyze:", ["Select"] + list(df.columns))

    def calculate_stats(column):
        column_data = df[column]

        # Categorical column handling
        if column_data.dtype == 'object':
            st.warning("⚠️ Mean and Median are not applicable to categorical data. Showing only Mode.")
            return None, None, column_data.mode().iloc[0]

        # Date column handling
        elif np.issubdtype(column_data.dtype, np.datetime64):
            numeric_dates = column_data.dropna().astype(np.int64)
            if len(numeric_dates) == 0:
                return None, None, None
            mean_val = pd.to_datetime(np.mean(numeric_dates))
            median_val = pd.to_datetime(np.median(numeric_dates))
            mode_val = column_data.mode().iloc[0]
            return mean_val, median_val, mode_val

        # Numeric column handling
        else:
            mean_val = column_data.mean()
            median_val = column_data.median()
            mode_val = column_data.mode().iloc[0]
            return mean_val, median_val, mode_val

    # Step 4: Display results and plot
    if column_name != "Select":
        mean_val, median_val, mode_val = calculate_stats(column_name)

        if mean_val is not None:
            st.success(f"**Mean:** {mean_val}")
            st.info(f"**Median:** {median_val}")
        if mode_val is not None:
            st.warning(f"**Mode:** {mode_val}")

        # Step 5: Plotting
        fig, ax = plt.subplots()

        # Date column plot
        if np.issubdtype(df[column_name].dtype, np.datetime64):
            date_counts = df[column_name].value_counts().sort_index()
            ax.bar(date_counts.index, date_counts.values, color='skyblue')
            ax.axvline(mean_val, color='red', linestyle='dashed', linewidth=2, label='Mean')
            ax.axvline(median_val, color='green', linestyle='dashed', linewidth=2, label='Median')
            ax.axvline(mode_val, color='orange', linestyle='dashed', linewidth=2, label='Mode')
            ax.set_title(f'Date Distribution of {column_name}')
            ax.set_xlabel("Date")
            ax.set_ylabel("Frequency")
            ax.legend()
            plt.xticks(rotation=45)

        # Categorical column plot
        elif df[column_name].dtype == 'object':
            cat_counts = df[column_name].value_counts()
            ax.bar(cat_counts.index, cat_counts.values, color='lightgreen')
            ax.set_title(f"Category Distribution of {column_name}")
            ax.set_xlabel(column_name)
            ax.set_ylabel("Count")
            plt.xticks(rotation=45)

        # Numeric column plot
        else:
            ax.hist(df[column_name].dropna(), bins=10, alpha=0.7, color='blue')
            ax.axvline(mean_val, color='red', linestyle='dashed', linewidth=2, label='Mean')
            ax.axvline(median_val, color='green', linestyle='dashed', linewidth=2, label='Median')
            ax.axvline(mode_val, color='orange', linestyle='dashed', linewidth=2, label='Mode')
            ax.set_title(f'Distribution of {column_name}')
            ax.set_xlabel(column_name)
            ax.set_ylabel("Frequency")
            ax.legend()

        # Show plot
        st.pyplot(fig)

else:
    st.info("📂 Please upload an Excel file to get started.")
