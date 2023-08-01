import streamlit as st
import pandas as pd
import plotly.express as px
import openpyxl
import matplotlib.pyplot as plt
import numpy as np
st.set_page_config(page_title='Kcc Sales Dashboard', layout='wide', page_icon=":bar_chart:")
data = pd.read_excel("G:\\tableau\\machinelearning\\kcc sales data.xlsx", sheet_name="Data")
data['year'] = pd.DatetimeIndex(data['Date']).year
data['year'] = data['year'].apply(str)

country = st.sidebar.multiselect(
    "select the Country Here: ",
    options=data['Country'].unique(),
    default=data['Country'].unique()
)
year = st.sidebar.multiselect(
    "select the Year Here: ",
    options=data['year'].unique(),
    default=data['year'].unique()
)
product = st.sidebar.multiselect(
    "select the Products Here: ",
    options=data['Product'].unique(),
    default=data['Product'].unique()
)

df_selection = data.query(
    "Country==@country&year==@year& Product==@product"
)
st.title(f":bar_chart: Kcc Performance Dashboard ")
st.markdown("***")
total_sales = int(df_selection['Revenue'].sum())
total_profit = int(df_selection['Profit'].sum())
total_Units_Sold = int(df_selection['Units Sold'].sum())
left, right, middle = st.columns(3)
with left:
    st.subheader(" Total Revenue")
    st.subheader(f"${total_sales}")
with right:
    st.subheader("total Profit")
    st.subheader(f"${total_profit}")
with middle:
    st.subheader("Number of Units Sold")
    st.subheader(f"${total_Units_Sold}")

st.markdown("---")
sales_by_product_line = df_selection.groupby(['Product']).agg({'Cost': 'mean', 'Profit': 'mean'}).reset_index()

res = px.bar(sales_by_product_line, x='Cost', y='Product', orientation='h', title='<b>Average Cost By Product<b>',
             template="plotly_white")
res.update_layout(plot_bgcolor="white", xaxis=(dict(showgrid=False)))
res.update_traces(text=sales_by_product_line['Cost'],textposition='inside',textfont=dict(size=16))

res2 = px.bar(sales_by_product_line, x='Product', y='Profit', orientation='v', title='<b>Average Profit By Product<b>',
              template="plotly_white")
res2.update_layout(yaxis=(dict(showgrid=False)),xaxis=(dict(tickangle=90)))
res2.update_traces(text=sales_by_product_line['Profit'],textposition='auto',textfont=dict(size=20))
left_column, right_column = st.columns(2)
left_column.plotly_chart(res2, use_container_width=True)
right_column.plotly_chart(res, use_container_width=True)
st.dataframe(df_selection)
hide_st_style="""
<style>
#Mainmenu{visiblity:hidden;}
footer{visiblity:hidden}
header{visiblity:hidden}
"""
st.markdown(hide_st_style,unsafe_allow_html=True)
