import streamlit as st
import pandas as pd
import numpy as np
from screens.add_expense import add_expenses
from screens.view_expense import view_expense
from screens.overview import overview_tab

if 'expense_categories' not in st.session_state:
    st.session_state.expense_categories = []

[viewExpensesTab, addExpensesTab, OverviewTab] = st.tabs(['View Expenses', 'Add Expenses', 'Overview Tab'])

with viewExpensesTab:
    view_expense()

with addExpensesTab: 
    add_expenses()

with OverviewTab:
    overview_tab()

