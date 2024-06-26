import streamlit as st
import datetime
import pandas as pd
import matplotlib.pyplot as plt

# Initialize the expense categories if not already in session state
if 'expense_categories' not in st.session_state:
    st.session_state.expense_categories = ['Food', 'Travel', 'Bills']

def renderDatePicker():
    """
    This function displays a date input inside of the page, and then returns the selected date.
    """
    expense_date = st.date_input("When was this expense?", datetime.date.today())
    return expense_date

def renderCategoryPicker():
    options = st.session_state.expense_categories + ["+ New Category"]
    col1, col2 = st.columns([2, 1])
    with col1:
        selection = st.selectbox("Select an option", options)
    if selection == "+ New Category":
        with col2:
            new_option = st.text_input("Enter new category")
            if new_option:
                st.session_state.expense_categories.append(new_option)
                st.success(f'New category "{new_option}" added.')
                selection = new_option
    return selection

def add_expenses():
    st.title("Add new expense")
    expense_date = renderDatePicker()
    expense_name = st.text_input("Expense Name:")
    expense_value = st.number_input("Expense Value:", min_value=0.0)
    expense_category = renderCategoryPicker()

    if st.button("Add Expense"):
        new_expense = {
            'Date': expense_date,
            'Name': expense_name,
            'Value': expense_value,
            'Category': expense_category
        }
        add_expense_to_csv(new_expense)
        st.success("Expense added successfully!")
        display_expense_plot()

def add_expense_to_csv(expense, filepath=None):
    """
    Adds a new expense to the expenses.csv file.
    """
    try:
        df = pd.read_csv('expenses.csv')
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Date', 'Name', 'Value', 'Category'])
    
    new_expense_df = pd.DataFrame([expense])
    df = pd.concat([df, new_expense_df], ignore_index=True)
    df.to_csv('expenses.csv', index=False)

def display_expense_plot():
    """
    Reads the expenses from the CSV file and displays a bar plot.
    """
    try:
        df = pd.read_csv('expenses.csv')
        if df.empty:
            st.write("No expenses to display.")
            return
        
        fig, ax = plt.subplots()
        df.groupby('Category')['Value'].sum().plot(kind='bar', ax=ax)
        ax.set_title('Total Expenses by Category')
        ax.set_xlabel('Category')
        ax.set_ylabel('Total Expense Value')
        st.pyplot(fig)
    except FileNotFoundError:
        st.write("No expenses to display.")

# Add expenses and display plotz
