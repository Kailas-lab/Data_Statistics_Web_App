import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Sample data
data = {
    "Region": ["North", "South", "East", "West", "North", "South", "East", "West", "North", "East"],
    "Item": ["Item1", "Item2", "Item3", "Item1", "Item2", "Item3", "Item1", "Item2", "Item3", "Item1"],
    "Order Date": pd.to_datetime([
        "2025-04-01", "2025-04-02", "2025-04-03", "2025-04-04", "2025-04-05",
        "2025-04-06", "2025-04-07", "2025-04-08", "2025-04-09", "2025-04-10"
    ])
}

df = pd.DataFrame(data)

st.title("📊 Data Statistics Web App")

# Dropdown for column selection
column_name = st.selectbox("Select a column:", ["Select", "Region", "Item", "Order Date"])

def calculate_stats(column_name):
    column_data = df[column_name]

    # Handle categorical
    if column_name in ["Region", "Item"]:
        st.warning("Mean and Median are not applicable to categorical data. Showing only Mode.")
        return None, None, column_data.mode().iloc[0]

    # Handle datetime
    elif np.issubdtype(column_data.dtype, np.datetime64):
        column_data_numeric = column_data.astype(np.int64)
        mean_val = pd.to_datetime(np.mean(column_data_numeric))
        median_val = pd.to_datetime(np.median(column_data_numeric))
        mode_val = column_data.mode().iloc[0]
        return mean_val, median_val, mode_val

    # Handle numeric
    else:
        mean_val = column_data.mean()
        median_val = column_data.median()
        mode_val = column_data.mode().iloc[0]
        return mean_val, median_val, mode_val

if column_name != "Select":
    mean_val, median_val, mode_val = calculate_stats(column_name)

    if mean_val is not None:
        st.success(f"**Mean:** {mean_val}")
        st.info(f"**Median:** {median_val}")
    st.warning(f"**Mode:** {mode_val}")

    # Plotting
    fig, ax = plt.subplots()

    if np.issubdtype(df[column_name].dtype, np.datetime64):
        # Bar plot for dates
        date_counts = df[column_name].value_counts().sort_index()
        ax.bar(date_counts.index, date_counts.values, color='skyblue', edgecolor='black')
        if mean_val is not None:
            ax.axvline(mean_val, color='red', linestyle='dashed', linewidth=2, label='Mean')
            ax.axvline(median_val, color='green', linestyle='dashed', linewidth=2, label='Median')
        ax.axvline(mode_val, color='orange', linestyle='dashed', linewidth=2, label='Mode')
        ax.set_title(f'Date Distribution of {column_name}')
        ax.set_xlabel("Date")
        ax.set_ylabel("Frequency")
        ax.legend()
        plt.xticks(rotation=45)
    else:
        # Bar/histogram for categorical or numeric
        if column_name in ["Region", "Item"]:
            cat_counts = df[column_name].value_counts()
            ax.bar(cat_counts.index, cat_counts.values, color='lightgreen')
            ax.set_title(f"Category Distribution of {column_name}")
            ax.set_xlabel(column_name)
            ax.set_ylabel("Count")
        else:
            ax.hist(df[column_name], bins=10, alpha=0.7, color='blue')
            ax.axvline(mean_val, color='r', linestyle='dashed', linewidth=2, label='Mean')
            ax.axvline(median_val, color='g', linestyle='dashed', linewidth=2, label='Median')
            ax.axvline(mode_val, color='y', linestyle='dashed', linewidth=2, label='Mode')
            ax.set_title(f'Distribution of {column_name}')
            ax.set_xlabel(column_name)
            ax.set_ylabel('Frequency')
            ax.legend()

    st.pyplot(fig)
