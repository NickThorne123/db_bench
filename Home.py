import streamlit as st
from st_pages import Page, Section, add_page_title, show_pages
from PIL import Image

st.set_page_config(
    page_title="Home | DB Bench",
    page_icon="./icons/pageIcon.png"
)

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
show_pages(
    [
        Page("Home.py", "Home", ""),
        Page("pages/ClickhouseDB.py", "ClickhouseDB", ""),
        Page("pages/PostgresqlDB.py", "PostgreSQL", ""),
        Page("pages/TimescaleDB.py", "TimescaleDB", ""),
        Page("pages/ArcticDB.py", "ArcticDB", "")
    ]
)

col1, col2 = st.columns([1,7])
with col1:
    st.image("./icons/pageIcon.png", width=70)
with col2:
    st.markdown("<h1 style='text-align: left;'>Database Benchmarking</h1>", unsafe_allow_html=True)

    
st.write("""This application is a streamlit web app which plots scalar values over time, 
             with a start / end datetime picker and a database source picker. Created by students at Southampton Solent University for one of our modules, 
             these students are:
             Josh Clarke, Daniel Agha, Iona Pitt, Kyle Roberts and Luke Wood""")
    
st.write("The database source options for this application are:")

col3, col4 = st.columns([1,10])
with col3:
    st.image("./icons/clickhouseLogo.png", width=45)
with col4:
    st.markdown("<h3 style='text-align: left;'>ClickhouseDB</h3>", unsafe_allow_html=True)

with col3:
    st.image("./icons/postgresqlLogo.png", width=45)
with col4:
    st.markdown("<h3 style='text-align: left;'>PostgreSQL</h3>", unsafe_allow_html=True)

with col3:
    st.image("./icons/TimescaleLogo.png", width=45)
with col4:
    st.markdown("<h3 style='text-align: left;'>TimescaleDB</h3>", unsafe_allow_html=True)

with col3:
    st.image("./icons/arcticLogo.png", width=45)
with col4:
    st.markdown("<h3 style='text-align: left;'>ArcticDB</h3>", unsafe_allow_html=True)

st.write("On each page there is: ")
st.markdown("- A date and time picker, for the start / end date that the data is plotted")
st.markdown("- A submit button that when pressed fetches the data for the plot")
st.markdown("- A ‘downsampling on-off’ toggle")
st.markdown("- A downsampling count text entry.")


st.write("""
                Further to this, on pressing the ‘submit’ button a timer is started that times how long it takes to fetch the data, 
                this will not include the time taken for the charting library to load it. 
                
                The elapsed time will be displayed on the dashboard near the line chart.
         
                Text boxes will be populated showing the space taken up on disk for the table, 
                and the number of rows in the table. 
         
                A text box showing GB of disk storage per million rows will be shown.
                """)
