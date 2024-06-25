import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
def overview_tab():
    st.title('At a Glance')
    getyearlydata()

def getyearlydata ():
    Months=[]
    Expensetotal=[]
    Budgettable=[]

    for filenames in os.walk ('data'):
        print(filenames[2])
        for i in filenames [2]: 
            data=pd.read_excel('data/'+i)
            expensesum= sum(data['Expense Value'])
            Expensetotal.append(expensesum)
            Budget=data.get('Budget')[0]
            print(Budget)
            Budgettable.append(Budget)
            print (Expensetotal)
            print (expensesum)
            [month, year] = i.split('_')
            Months.append(month)
            if expensesum > 1000:
                st.error(f'budget exceeded for the month {month}')
            else: 
                st.balloons()
            year = year.split ('.') [0]
            print (year)
    fig, ax = plt.subplots()
    ax.set_title('Monthly Expenses and Budget')
    ax.set_xlabel('Months')
    index=np.arange(len(Months))
    bar1 = ax.bar (index,Expensetotal,label='Expenses', width=0.25)
    bar1 = ax.bar (index+0.25,Budgettable,label='Budget', width=0.25)
    ax.set_ylabel('Amount Spent')
    ax.set_xticks(index+0.25/2)
    ax.set_xticklabels(Months)
    st.pyplot(fig)
