import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import calendar


def overview_tab():
    st.title('At a Glance')
    getyearlydata()

def render_elements_on_page(sorted_months, sorted_expense_total, sorted_budget_total):
    fig, ax = plt.subplots()
    ax.set_title('Monthly Expenses and Budget')
    ax.set_xlabel('Months')
    index = np.arange(len(sorted_months))
    ax.bar(index, sorted_expense_total, label='Expenses', width=0.25)
    ax.bar(index + 0.25, sorted_budget_total, label='Budget', width=0.25)
    ax.set_ylabel('Amount Spent')
    ax.set_xticks(index + 0.25 / 2)
    ax.set_xticklabels(sorted_months)
    plt.xticks(rotation=90)
    ax.legend()
    st.pyplot(fig)

def create_data(months, expense_total, budget_total):
    data = pd.DataFrame({
        'Month': months,
        'Expense': expense_total,
        'Budget': budget_total
    })
    month_order = list(calendar.month_name)[1:]  # ['January', 'February', ..., 'December']
    data['Month'] = data['Month'].apply(lambda x: x.capitalize())
    data['Month'] = pd.Categorical(data['Month'], categories=month_order, ordered=True)
    data = data.sort_values('Month')
    sorted_months = data['Month'].tolist()
    sorted_expense_total = data['Expense'].tolist()
    sorted_budget_total = data['Budget'].tolist()
    return sorted_months, sorted_expense_total, sorted_budget_total

@st.cache_data
def getyearlydata():
    months = []
    expense_total = []
    budget_total = []
    for root, dirs, files in os.walk('data'):
        for i in files: 
            data = pd.read_excel(os.path.join(root, i))
            expensesum = sum(data['Expense Value'])
            expense_total.append(expensesum)
            budget = data.get('Budget')
            if budget is not None:
                budget = budget.iloc[0]
            else:
                budget = 0  # Or some other default value
            budget_total.append(budget)
            [month, year] = i.split('_')
            month = month.strip()
            months.append(month)
            year = year.split('.')[0]
            if st.session_state.page == 'Overview':
                if expensesum > budget:
                    st.toast(f'Budget exceeded for the month of {month}', icon="🚨")
                else: 
                    st.balloons()
    
    # Create a DataFrame for easier sorting
    sorted_months, sorted_expense_total, sorted_budget_total = create_data(months, expense_total, budget_total)
    
    render_elements_on_page(sorted_months, sorted_expense_total, sorted_budget_total)
