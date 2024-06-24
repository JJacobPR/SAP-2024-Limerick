import os

import streamlit as st
import pandas as pd
import numpy as np


# Function to read and display the Excel file
def read_expenses(file_path):
    try:
        # Read the Excel file into a DataFrame
        expenses_df = pd.read_excel(file_path)

        # Display the first few rows of the DataFrame
        print("First few rows of the expense data:")
        print(expenses_df.head())

        return expenses_df
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")




st.title('Expense Overview')

expense_year = st.selectbox(
    "Select year",
    ("2024", "2025", "2026", "2027", "2028", "2029", "2030"))

expense_month = st.selectbox(
    "Select month",
    ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"))

if expense_year != '' and expense_month != '':
    file_path = f'data/{expense_month}_{expense_year}.xlsx'
    if os.path.exists(file_path):
        st.subheader(read_expenses(file_path))
    else:
        st.subheader("No data for chosen month available, please upload a file")

