import streamlit as st
from database.prediction_repository import PredictionRepository

repo = PredictionRepository()

# Import custom functions/pages from other Python files
from welcome import show_welcome_page
from app import show_main_app

# Set the page title, tab icon, and wide layout (Must be at the top)
st.set_page_config(page_title='Uber Fare Predictor' , page_icon='🚖' , layout='wide')

# Initialize the 'page' variable only once on the first app load
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'

# Simple Routing for the page based on the current session state
if st.session_state.page =='welcome':
    show_welcome_page()
elif st.session_state.page == 'app' :
    show_main_app()

        

    
  

