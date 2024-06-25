import streamlit as st
import datetime

def renderDatePicker():
    """
        This function displays a date input inside of the page, and then returns the selected date
    """
    expense_date = st.date_input("When was this expense? ", datetime.date.today())
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
    else:
        col2.write("")

def add_expenses():
    st.title("Add new expense")
    expense_date = renderDatePicker()
    st.text_input("Expense Name: ")
    st.number_input("Expense Value: ", min_value=0)
    renderCategoryPicker()