import streamlit as st
import pandas as pd
import numpy as np
from screens.add_expense import add_expenses
from screens.view_expense import view_expense

if 'expense_categories' not in st.session_state:
    st.session_state.expense_categories = []

[viewExpensesTab, addExpensesTab] = st.tabs(['View Expenses', 'Add Expenses'])

with viewExpensesTab:
    view_expense()

with addExpensesTab: 
    add_expenses()
