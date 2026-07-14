import streamlit as st
import folium 
from streamlit_folium import st_folium 
from geopy.geocoders import Nominatim   # to convert text to cooardinates
import numpy as np
import pandas as pd
import joblib
import os


try:
    from database.prediction_repository import PredictionRepository
    repo = PredictionRepository()
except Exception:
    repo = None

@st.cache_resource
def load_best_model():
    model_path = os.path.join(os.path.dirname(__file__), 'best_model.joblib')
    
    if os.path.exists(model_path):
        return joblib.load(model_path)
    return None






def show_main_app():

    AIRPORTS = {
    'JFK': (40.6413, -73.7781),
    'LGA': (40.7769, -73.8740),
    'EWR': (40.6895, -74.1745)}

    CENTER_LAT = 40.7580
    CENTER_LON = -73.9855

    # Initialize geocoder to convert text addresses into coordinates
    geolocator = Nominatim(user_agent="uber_fare_predictor_app")

    # ==============================================================================
    # SECTION 1: FEATURE ENGINEERING & HELPER FUNCTIONS
    # ==============================================================================

    def haversine_distance(lat1, lon1, lat2, lon2):
     #Earth's radius in km
     R = 6371
     #converting deg to rad
     lat1 = np.radians(lat1)
     lon1 = np.radians(lon1)
     lat2 = np.radians(lat2)
     lon2 = np.radians(lon2)

      #calculating differences
     dlat = lat2 - lat1
     dlon = lon2 - lon1

      #Haversin formula
     a = np.sin(dlat / 2) **2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
     c = 2 * np.arcsin(np.sqrt(a))

     return R * c
    
    def is_airport_trip (lat , lon , threshold_km = 5.0):
        for airport , (a_lat , a_lon) in AIRPORTS.items():
            distance = haversine_distance(lat , lon , a_lat , a_lon)

            if distance <= threshold_km :
                return 1  
        return 0  
    
    def get_features_for_model(p_lat,p_lon,d_lat,d_lon,pickup_year=2026):

        #Distance
        trip_distance_km = haversine_distance(p_lat,p_lon,d_lat,d_lon)
        manhattan_distance = (abs(p_lat - d_lat) + abs(p_lon - d_lon)) * 111.0
        displacement_ratio = manhattan_distance / (trip_distance_km+ 1e-5)


        #Airport
        is_pickup_airport = is_airport_trip(p_lat,p_lon)
        is_dropoff_airport = is_airport_trip(d_lat,d_lon)
        if (is_pickup_airport == 1 or is_dropoff_airport == 1):
            is_airport = 1
        else:
            is_airport = 0
        

        #Bearing
        lat1, lon1 = np.radians(p_lat), np.radians(p_lon)
        lat2, lon2 = np.radians(d_lat), np.radians(d_lon)
        dlon = lon2 - lon1
        x = np.sin(dlon) * np.cos(lat2)
        y = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(dlon)
        bearing = np.degrees(np.arctan2(x, y))

        #Center
        pickup_to_center_km = haversine_distance(p_lat, p_lon, CENTER_LAT, CENTER_LON)
        dropoff_to_center_km = haversine_distance(d_lat, d_lon, CENTER_LAT, CENTER_LON)
        avg_distance_to_center = (pickup_to_center_km + dropoff_to_center_km) / 2.0

        
        feature_df = pd.DataFrame([{
            'pickup_year' : pickup_year,
            'bearing'     : bearing,
            'avg_distance_to_center' : avg_distance_to_center,
            'is_airport'  : is_airport,
            'manhattan_distance' : manhattan_distance,}])
    
        return feature_df,trip_distance_km, bearing, is_airport , avg_distance_to_center , manhattan_distance ,displacement_ratio
    
     
    def get_address_from_coords (lat , lon):
       #Converts (lat, lng) coordinates into a human-readable address.
        try :
          location = geolocator.reverse((lat,lon) , timeout= 10)
          if location and location.address:
             return location.address.split(",")[0] + ", " + location.address.split(",")[1]
        except Exception:
           pass
        return f"{lat:.4f}, {lon:.4f}"
       



 # ==============================================================================
                         # SECTION 4: STREAMLIT APP UI 
 # ==============================================================================

    # back button
    if st.button("🔙 Back to Welcome"):
        st.session_state.page = "welcome"
        st.rerun()

    st.title ("🚖 Uber Fare & Route Estimator")
    st.write("Select pickup and dropoff points from the map or type the addresses directly.")

    # Initializing Session States
    if 'pickup' not in st.session_state:
     st.session_state.pickup = [40.7580, -73.9855]  # Times Square
    if "dropoff" not in st.session_state:
     st.session_state.dropoff = [40.6413, -73.7781] # JFK Airport
    if "map_center" not in st.session_state:
     st.session_state.map_center = [40.7580, -73.9855]
    if "pickup_text_val" not in st.session_state:
        st.session_state.pickup_text_val = "Times Square, NYC"
    if "pickup_key_counter" not in st.session_state:
        st.session_state.pickup_key_counter = 0

    if "dropoff_text_val" not in st.session_state:
        st.session_state.dropoff_text_val = "JFK Airport, NYC"
    if "dropoff_key_counter" not in st.session_state:
        st.session_state.dropoff_key_counter = 0
    if "prev_dropoff_text" not in st.session_state:
     st.session_state.prev_dropoff_text = ""


    if "prev_pickup_text" not in st.session_state:
     st.session_state.prev_pickup_text = ""
    
    col_map , col_setting = st.columns([5,1])

    with col_setting:
     st.subheader("📍 Trip Settings")
     cotrol , _ = st.columns(2)
     with cotrol :
        point_mode = st.radio("Map Click Mode (Select which pin to drop on click):",
                              ["Pickup Location 🟢", "Dropoff Location 🔴"] , index = 0)

    with col_map :
       # Build Folium Map centered around computed center
       m = folium.Map(location= st.session_state.map_center , zoom_start=11)
       
       # Place Marker 
       folium.Marker(location= st.session_state.pickup , popup="Pickup" , icon= folium.Icon(color="green" , icon="car" ,prefix='fa')).add_to(m)
       folium.Marker(location= st.session_state.dropoff , popup="Dropoff" , icon= folium.Icon(color="red" , icon="car" ,prefix='fa')).add_to(m)

       # Draw path
       folium.PolyLine(locations=[st.session_state.pickup , st.session_state.dropoff],color="blue", weight=3, opacity=0.7).add_to(m)

       # Display Map
       map_data = st_folium ( m , width = '100%' , height =400)

        # Update coordinates dynamically when map is clicked
       if map_data and map_data.get('last_clicked'):
          clicked_lat = map_data['last_clicked']['lat']
          clicked_lng = map_data['last_clicked']['lng']
          
          if "Pickup" in point_mode :
             if st.session_state.pickup != [clicked_lat , clicked_lng] :
              address_name = get_address_from_coords(clicked_lat , clicked_lng)
              st.session_state.pickup = [clicked_lat , clicked_lng]
              st.session_state.pickup_text_val = address_name
              st.session_state.pickup_key_counter += 1
              st.session_state.map_center = [clicked_lat, clicked_lng]
              st.rerun()

          else:
              if st.session_state.dropoff != [clicked_lat, clicked_lng]:
                    address_name = get_address_from_coords(clicked_lat, clicked_lng)
                    st.session_state.dropoff = [clicked_lat, clicked_lng]
                    st.session_state.dropoff_text_val = address_name
                    st.session_state.dropoff_key_counter += 1
                    st.session_state.map_center = [clicked_lat, clicked_lng]
                    st.rerun()

    st.subheader("🔍 Search Locations :")
    search1 , search2 = st.columns(2)

    with search1 :
       pickup_input = st.text_input("Enter Pickup Address (e.g., Central Park, NYC):" ,value=st.session_state.pickup_text_val,key=f"pickup_box_{st.session_state.pickup_key_counter}")

    if pickup_input and pickup_input.strip() != st.session_state.pickup_text_val:
        try:
           
         location = geolocator.geocode(pickup_input , timeout= 10)
         if location:
              st.session_state.pickup = [location.latitude , location.longitude]
              st.session_state.map_center = [location.latitude , location.longitude]
              st.session_state.pickup_text_val = pickup_input
              st.toast("🟢 Pickup location updated!", icon="✅")
              st.rerun()
             
         else:
             st.error("Location not found. Please try again with more details.")
        except Exception:
          st.error("Service busy, please try again.")

          
    with search2 :
       dropoff_input = st.text_input(
            "Enter Dropoff Address (e.g., JFK Airport):", value=st.session_state.dropoff_text_val,
            key=f"dropoff_box_{st.session_state.dropoff_key_counter}"
        )

       if dropoff_input and dropoff_input.strip() != st.session_state.prev_dropoff_text:
            try:
                location = geolocator.geocode(dropoff_input , timeout=10)
                if location:
                    st.session_state.dropoff = [location.latitude , location.longitude]
                    st.session_state.map_center = [location.latitude , location.longitude]
                    st.session_state.prev_dropoff_text = dropoff_input 
                    st.toast("🔴 Dropoff location updated!", icon="✅")
                    st.rerun()
                else:
                    st.error("Location not found. Please try again.")
            except Exception:
                st.error("Service busy, please try again.")

      # ==============================================================================
                  # SECTION 5: FARE PREDICTION & RESULTS DISPLAY
      # ==============================================================================
       st.markdown("---")
    
    if st.button("💰 Calculate Estimated Fare & Distance "):
         
            p_lat, p_lng = st.session_state.pickup
            d_lat, d_lng = st.session_state.dropoff

           
            
            input_df, trip_distance, bearing, is_airport , avg_distance_to_center , manhattan_distance ,displacement_ratio= get_features_for_model(p_lat, p_lng, d_lat, d_lng)
            
            model = load_best_model()
            try:
                predicted_price = model.predict(input_df)[0]

                # ------------------------------------------------------------------
                # 🟢 2. حفظ التوقع في الداتابيز بسكوت التام (في الخفاء)
                # ------------------------------------------------------------------
                if repo is not None:
                    try:
                        repo.save_prediction(
                            pickup_lat=p_lat,
                            pickup_lon=p_lng,
                            dropoff_lat=d_lat,
                            dropoff_lon=d_lng,
                            pickup_datetime="2026-01-01 00:00:00",
                            passenger_count=1,
                            trip_distance_km=trip_distance,
                            bearing=bearing,
                            avg_distance_to_center=avg_distance_to_center,
                            is_airport=is_airport,
                            hour_sin=0.0,
                            hour_cos=1.0,
                            manhattan_distance=manhattan_distance,
                            displacement_ratio=displacement_ratio,
                            predicted_fare=float(predicted_price)
                        )
                    except Exception:
                        pass  # يتجاهل أي خطأ في الداتابيز لضمان الاستمرارية

           

                
                with st.container(border=True):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                     st.markdown(f"""
                        <div style="background-color: #d1ecf1; border-left: 5px solid #17a2b8; padding: 12px 15px; border-radius: 8px; margin-bottom: 10px;">
                            <span style="font-size: 18px; font-family: 'Poppins', sans-serif; color: #0c5460; font-weight: bold;">
                                💰 Estimated Fare:
                            </span>
                            <span style="font-size: 22px; font-family: 'Poppins', sans-serif; color: #0c5460; font-weight: 800; margin-left: 8px;">
                                {float(predicted_price):.2f} $
                            </span>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    with col2:
                     st.markdown(f"""
                        <div style="background-color: #d1ecf1; border-left: 5px solid #17a2b8; padding: 12px 15px; border-radius: 8px; margin-bottom: 10px;">
                            <span style="font-size: 18px; font-family: 'Poppins', sans-serif; color: #0c5460; font-weight: bold;">
                                🚕Trip Distance:
                            </span>
                            <span style="font-size: 20px; font-family: 'Poppins', sans-serif; color: #0c5460; font-weight: 800; margin-left: 8px;">
                                {trip_distance:.2f} km
                            </span>
                        </div>
                        """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error making prediction: {e}")
           

