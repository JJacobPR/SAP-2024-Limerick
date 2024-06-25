import streamlit as st
import os
import pandas as pd

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

def view_expense():
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

                col1, col2, col3 = st.columns(3)

                with col1:
                    selected_category = st.selectbox(
                        "Select Expense Category",
                        ["All"] + st.session_state.expense_categories
                    )

                with col2:
                    st.text("")
                    st.text("")
                    selected_essential = st.checkbox("Essential", False)

                with col3:
                    st.text("")
                    st.text("")
                    selected_non_essential = st.checkbox("Non Essential", False)

                # Filtering by necessity
                if selected_essential and selected_non_essential:
                    filtered_expenses = expenses
                elif selected_essential:
                    filtered_expenses = expenses[expenses['Expense Necessity'] == "Essential"]
                elif selected_non_essential:
                    filtered_expenses = expenses[expenses['Expense Necessity'] == "Non-Essential"]
                else:
                    filtered_expenses = expenses

                # Filtering by category
                if selected_category != "All":
                    filtered_expenses = filtered_expenses[expenses['Expense Category'] == selected_category]
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
    