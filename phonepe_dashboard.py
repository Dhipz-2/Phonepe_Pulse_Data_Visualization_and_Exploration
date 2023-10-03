import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
import plotly.graph_objects as go
import json

hostname = 'localhost'
database = 'phonepe_db'
username = 'postgres'
pwd = ''
port_id = 5432

conn = psycopg2.connect(
    host = hostname,
    dbname = database,
    user = username,
    password = pwd,
    port = port_id
)

cur = conn.cursor()

#DASHBOARD

base="light"
primaryColor="#252224"
secondaryBackgroundColor="#f3d7ee"
textColor="#542f71"
font="serif"


st.set_page_config(layout="wide")
st.header("PHONEPE PULSE DATA VISUALIZATION AND EXPLORATION",divider='grey')

box = st.sidebar.selectbox(
    "**TRANSACTION OR USER**",
    ('Transaction', 'User')
)

year = st.sidebar.selectbox(
    "**Select Year**",
    ('2018','2019','2020','2021','2022')
)

quarter = st.sidebar.radio(
    "**Select Quarter**",
    ("Q1", "Q2", "Q3", "Q4")
)


tab1, tab2, tab3 = st.tabs(["**Payment transaction and Users Device**".center(20,"\u2001"), 
                                  "**Statewise Transactions**".center(40,"\u2001"), 
                                  "**Top States**".center(10,"\u2001")])


if quarter=='Q1':
    quarter = 1
elif quarter=='Q2':
    quarter = 2
elif quarter=='Q3':
    quarter = 3
else:
    quarter = 4
with tab1:
    
    if box=='Transaction':
        payment_options = st.selectbox("**Select Transaction type**",
                                    ("Recharge & bill payments", "Peer-to-peer payments", "Merchant payments", "Financial Services","Others"))
        try:
            cur.execute(f"select transaction_name, number_of_transactions, transaction_amount, state from transaction_type where year ={year} and quater={quarter} and transaction_name ='{payment_options}';")
            sql = cur.fetchall()
            df = pd.DataFrame(sql, columns=['Transaction_type','Total_transactions', 'Total_amount','State']).reset_index(drop=True)
            fig = px.bar(df, x='State', y='Total_transactions',
                        hover_data=['Transaction_type'], color='Total_amount',
                        color_continuous_scale='Agsunset', width = 1000, height=600)
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)

            cur.execute(f"select transaction_name, sum(number_of_transactions) from transaction_type where year ={year} and quater={quarter} group by transaction_name;")
            sql1 = cur.fetchall()
            df1 = pd.DataFrame(sql1, columns=['Transaction_Type','Total_transactions']).reset_index(drop=True)
            st.table(df1)

        except Exception as error:
            print(error)

    elif box=='User':
        try:
            cur.execute(f"select brand, registered_users, users_percentage, state from register_phone_users where year ={year} and quater={quarter};")
            sql = cur.fetchall()
            df = pd.DataFrame(sql, columns=['Users_by_device','Registered_users', 'Users_percentage','State']).reset_index(drop=True)
            fig = px.treemap(df, path=[px.Constant("India"), 'State', 'Users_by_device'], values='Registered_users',
                color='Registered_users', hover_data=['Users_percentage'],
                color_continuous_scale='Agsunset')
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)

            cur.execute(f"select brand, sum(registered_users) from register_phone_users where year ={year} and quater={quarter} group by brand;")
            sql1 = cur.fetchall()
            df1 = pd.DataFrame(sql1, columns=['Transaction_Type','Total_transactions']).reset_index(drop=True)
            st.table(df1)

        except Exception as error:
            print(error)

with tab2:
    if box=='Transaction':
        st.subheader("Statewise Transactions")
        cur.execute(f'select state, sum(number_of_transactions), sum(transaction_amount) from statelevel_transaction where year = {year} and quater = {quarter} group by state;')
        sql = cur.fetchall()
        df = pd.DataFrame(sql, columns=['State','Total_transactions','Total_amount'])
        df2 = pd.read_csv(r"C:\Users\Dhipika\Downloads\Statenames.csv")
        df.State = df2
        
        fig = px.choropleth(df, locations='State', geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM',color_continuous_scale='Agsunset',
                            color='Total_transactions', hover_data=['Total_amount'])
        fig.update_geos(fitbounds='locations', visible=False)
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    elif box=='User':
        st.subheader("Statewise Users")
        cur.execute(f'select state, sum(registered_user) from statelevel_users where year = {year} and quater = {quarter} group by state;')
        sql = cur.fetchall()
        df = pd.DataFrame(sql, columns=['State','Total_Users'])
        df2 = pd.read_csv(r"C:\Users\Dhipika\Downloads\Statenames.csv")
        df.State = df2
        
        fig = px.choropleth(df, locations='State', geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM',color_continuous_scale='Agsunset',
                            color='Total_Users')
        fig.update_geos(fitbounds='locations', visible=False)
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

with tab3:

    if box=='Transaction':
        st.subheader("Top 10 State Transactions")
        cur.execute(f'select state, sum(total_number_of_transactions), sum(total_transaction_amount) from top_transactions where year = {year} and quater = {quarter} group by state order by sum(total_number_of_transactions) desc limit 10;')
        sql = cur.fetchall()
        df = pd.DataFrame(sql, columns=['Top_State','Top_transactions', 'Total_amount'])

        fig=px.pie(df,names='Top_State', values='Top_transactions', hole = 0.4, color='Total_amount',
                   hover_data='Total_amount',color_discrete_sequence=px.colors.sequential.Agsunset, labels={'Top_State':'Top States'})
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

        st.table(df.iloc[:,:2])
        
    elif box=='User':
        st.subheader("Top 10 State Users")
        cur.execute(f'select state, sum(top_registered_users) from top_users where year = {year} and quater = {quarter} group by state order by sum(top_registered_users) desc limit 10;')
        sql = cur.fetchall()
        df = pd.DataFrame(sql, columns=['Top_State_Users','Top_Registered_Users'])

        fig=px.pie(df,names='Top_State_Users', values='Top_Registered_Users', hole = 0.4,
                   color_discrete_sequence=px.colors.sequential.Agsunset, labels={'Top_State_Users':'Top States Users'})
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        
        st.table(df)

conn.commit()
conn.close()
    

    

    
