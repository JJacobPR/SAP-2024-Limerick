import os
import streamlit as st
import pandas as pd
import numpy as np
import datetime

# Initialize session state for expense categories if not already done
if 'expense_categories' not in st.session_state:
    st.session_state.expense_categories = []

[tab1, tab2] = st.tabs(['View Expenses', 'Add Expenses'])

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

with tab1:
    st.title('Expense Overview')

    st.session_state.year = st.selectbox(
        "Select year",
        ("2024", "2025", "2026", "2027", "2028", "2029", "2030")
    )

    st.session_state.month = st.selectbox(
        "Select month",
        ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
    )

    if st.session_state.year and st.session_state.month:
        file_path = f'data/{st.session_state.month.lower()}_{st.session_state.year}.xlsx'
        if os.path.exists(file_path):
            expenses = read_expenses(file_path)
            if expenses is not None: 
                st.session_state.expense_categories = [cat for cat in expenses['Expense Category'].unique().tolist() if pd.notna(cat)]
                c1, c2 = st.columns(2)

                selected_category = st.selectbox(
                    "Select Expense Category",
                    ["All"] + st.session_state.expense_categories
                )

                if selected_category != "All":
                    filtered_expenses = expenses[expenses['Expense Category'] == selected_category]
                else:
                    filtered_expenses = expenses

                st.write(f"### {selected_category} expenses")
                st.dataframe(filtered_expenses, hide_index=True, use_container_width=True)
        else:
            st.subheader("No data for chosen month available, please upload a file")
            file = st.file_uploader("Choose a file", type="xlsx", accept_multiple_files=False)
            if file is not None:
                save_file_to_directory(file, 'data', f'{st.session_state.month.lower()}_{st.session_state.year}.xlsx')
                st.experimental_rerun()

def renderDatePicker():
    expense_date = st.date_input("When was this expense? ", datetime.date(2019, 7, 6))
    return expense_date

def renderCategoryPicker():
    # Append the "+ NEW" option to the list of expense categories
    options = st.session_state.expense_categories + ["+ NEW"]
    
    # Create two columns for the selectbox and the text input
    col1, col2 = st.columns([2, 1])
    
    # Create a selectbox with the options
    with col1:
        selection = st.selectbox("Select an option", options)
    
    # If "+ NEW" is selected, prompt the user to add a new option in the second column
    if selection == "+ NEW":
        with col2:
            new_option = st.text_input("Enter new category")
        
            # Add the new option to the list if it is not empty
            if new_option:
                st.session_state.expense_categories.append(new_option)
                st.success(f'New category "{new_option}" added.')
                # st.session_state.expense_categories + [new_option]
                # Re-render the selectbox with the updated list of categories
                # options = st.session_state.expense_categories + ["+ NEW"]
                # selection = st.selectbox("Select an option", options, index=len(options)-2)
                # st.rerun()
    else:
        col2.write("")  # Ensure the second column remains empty

with tab2: 
    st.title("Add new expense")
    expense_date = renderDatePicker()
    st.text_input("Expense Name: ")
    st.number_input("Expense Value: ", min_value=0)
    renderCategoryPicker()
