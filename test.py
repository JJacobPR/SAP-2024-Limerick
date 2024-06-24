import os

import streamlit as st
import pandas as pd
import numpy as np


# Function to read and display the Excel file
def read_expenses(file_path):
    try:
        # Read the Excel file into a DataFrame
        expenses_df = pd.read_excel(file_path)

        return expenses_df

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


def save_file_to_directory(file_path, save_dir, file_name):
    try:
        # Read the Excel file into a DataFrame
        df = pd.read_excel(file_path)

        # Ensure the save directory exists
        os.makedirs(save_dir, exist_ok=True)

        # Construct the full file path for saving
        save_path = os.path.join(save_dir, file_name)

        # Save the DataFrame to the specified path
        df.to_excel(save_path, index=False)

        print(f"File saved successfully at: {save_path}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


st.title('Expense Overview')

st.session_state.year = st.selectbox(
    "Select year",
    ("2024", "2025", "2026", "2027", "2028", "2029", "2030"))

st.session_state.month = st.selectbox(
    "Select month",
    ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"))

expense = [] 


if st.session_state.year != '' and st.session_state.month != '':
    file_path = f'data/{st.session_state.month.lower()}_{st.session_state.year}.xlsx'
    if os.path.exists(file_path):
        expenses = read_expenses(file_path)
        print(expenses)
        if expenses is not None: 
            for i in range(0, 52):
                expense_value = expenses.at[i, 'Expense Category']
                if expense_value not in expense:
                    expense.append(expense_value)
            
            print(f"Values inside {expense}")
            
            st.dataframe(
                expenses,
                hide_index=True,
                height=600,
                use_container_width=True,
                selection_mode=["expense"]
            )
    else:
        st.subheader("No data for chosen month available, please upload a file")
        file = st.file_uploader("Choose a file", type="xlsx", accept_multiple_files=False)
        if file is not None:
            save_file_to_directory(file, 'data', f'{st.session_state.month.lower()}_{st.session_state.year}.xlsx')
            st.rerun()
