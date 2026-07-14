import streamlit as st 
import base64


def get_base64_image(bin_file):
    # Open the image file in  read binary mode ('rb')
    with open(bin_file, 'rb') as file:
        data = file.read()            # Read the raw binary content of the file
        return base64.b64encode(data).decode()   # Convert binary data to a Base64 string to use it in CSS/HTML

def load_welcome_background(image_path):

 # Convert the image file into a Base64 encoded string
    img = get_base64_image(image_path)

 # Define custom CSS inside a Python f-string to style the Streamlit app
    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image:
        linear-gradient(
            rgba(0,0,0,0.45),
            rgba(0,0,0,0.45)
        ),
        url("data:image/jpg;base64,{img}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    /* CSS for Transparent Button */
    div.stButton > button {{
        background-color: transparent !important;
        color: white !important;
        border: 1px solid white !important;
        transition: 0.3s;
    }}

    div.stButton > button:hover {{
        background-color: rgba(255, 255, 255, 0.2) !important;
        border-color: white !important;
    }}

    [data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
    }}

    [data-testid="stSidebar"] {{
        background: rgba(0,0,0,0.3);
        backdrop-filter: blur(10px);
    }}

    h1, h2, h3, h4, h5, h6, p, label, div {{
        color: white;
    }}
    </style>
    """
    # Inject the custom CSS into the Streamlit application
    st.markdown(page_bg_img, unsafe_allow_html=True)



       
def show_welcome_page():
 # Load background image using the previously defined function
    load_welcome_background("background.png")

 # Render a centered white semi-transparent card containing the main title and description
    st.markdown(
        """
        <div style="
            background-color: rgba(255, 255, 255, 0.85);
            padding: 40px 30px;
            border-radius: 20px;
            box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
            max-width: 800px;
            margin: 40px auto;
            text-align: center;
        ">
            <h1 style="color: #1E3A8A; font-size: 45px; margin-bottom: 10px; font-weight: bold;">
                🚖 Welcome to Uber Taxi Application
            </h1>
            <p style="color: #4B5563; font-size: 18px; line-height: 1.6; margin-bottom: 30px;">
                Perfect way for real-time ride fare, distance, and duration estimations.
            </p>
        """, 
        unsafe_allow_html=True
    )
    
 # Divide page into 3 layout columns to center the content inside the middle column (col2)
    _ , col2 , _ = st.columns([1.5,1,1.5])
    
    with col2:
     # Display key features list using styled HTML span elements
     st.markdown(
     '<span style="font-size: 20px; font-family: Poppins, sans-serif; color: #ffffff; font-weight: bold">'
     '🗺️ Interactive Navigation'
     '</span>', 
     unsafe_allow_html=True
     )
    
     st.markdown(
         '<span style= "font-size: 20px; font-family : Poppins, sans-serif; color : #ffffff ; font-weight : bold  ">'
         '🚗 Distance Estimation'
         '</span>',
         unsafe_allow_html= True
     )

     st.markdown('<span style= "font-size: 20px; font-family : Poppins, sans-serif; color : #ffffff ; font-weight : bold  ">'
         '💰 Smart Fare AI'
         '</span>',
         unsafe_allow_html= True)
     


     st.write("")
     # Handle navigation button click to redirect user to the main application page
     if st.button("Start Trip Now 🚀", use_container_width=True):
            st.session_state.page = "app"
            st.rerun()
     # Close the custom HTML wrapper div 
     st.markdown("</div>", unsafe_allow_html=True)

    