
import streamlit as st
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
import pandas as pd
import twint
import base64
import datetime

st.set_page_config(layout="wide")
st.title('Twitter Scraper')

with st.form(key='Twitter_form'):
    search_term = st.text_input('Keywords search')
    limit = st.slider('How many tweets do you want to get?', 0, 10000, step=100)
    since = st.date_input("Start date", datetime.datetime(2021, 1, 1))
    until = st.date_input("End date", datetime.datetime(2021, 1, 31)) 
    likes = st.number_input('Minimum likes',step=1)   
    output_csv = st.radio('Save a CSV file?', ['Yes', 'No'])
    file_name = st.text_input('Name the CSV file:')
    submit_button = st.form_submit_button(label='Search')

    if submit_button:
        # configure twint
        c = twint.Config()
        c.Search = search_term
        c.Limit = limit
        c.Min_likes = likes
        c.Since = str(since)
        c.Until = str(until)
        c.Custom["tweet"] = ["id", "date", "time", "user_id", "username", "tweet", "likes_count"]
        c.Utc = True
        c.Full_text = True
        c.Store_csv = True

        if c.Store_csv:
            c.Output = f'{file_name}.csv'

        twint.run.Search(c)

        data = pd.read_csv(f'{file_name}.csv') #, usecols=['date', 'tweet'])

        #page = 1
        #page_limit = 10
        #dff = data[(int(page) - 1) * int(page_limit) : (int(page) * int(page_limit))]
        gd = GridOptionsBuilder.from_dataframe(data)
        gd.configure_pagination(enabled=True)
        gd.configure_default_column(editable=True,groupable=True)
        gridoptions = gd.build()
        AgGrid(data,gridOptions=gridoptions)

def convert_df(df):
    return df.to_csv().encode('utf-8')

try:
    st.download_button(label='Download results', data=convert_df(data), file_name = f'{file_name}.csv', mime='text/csv')
except:
    pass

def get_csv_download_link(csv, filename):

    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv">Download csv file</a>'
    return href