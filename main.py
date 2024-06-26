import streamlit as st
import pandas as pd
import numpy as np
from screens.add_expense import add_expenses
from screens.view_expense import view_expense
from screens.overview import overview_tab


st.set_page_config(
    page_title="Personal Finance Tracker",
    layout="centered",
    initial_sidebar_state="expanded",
)

if 'page' not in st.session_state:
    st.session_state.page = 'main'

if 'expense_categories' not in st.session_state:
    st.session_state.expense_categories = []

[viewExpensesTab, addExpensesTab, OverviewTab] = st.tabs(['View Expenses', 'Add Expenses', 'Overview Tab'])

with viewExpensesTab:
    st.session_state.page = 'View_Expenses'
    view_expense()

with addExpensesTab: 
    st.session_state.page = 'Add_Expense'
    add_expenses()

with OverviewTab:
    st.session_state.page = 'Overview'
    overview_tab()
