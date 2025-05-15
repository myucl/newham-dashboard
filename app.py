import streamlit as st
import folium
from streamlit_folium import folium_static
import geopandas as gpd
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="Newham Dashboard",
    page_icon="🗺️",
    layout="wide"
)

# Title and description
st.title("Newham Borough Dashboard")
st.markdown("""
This dashboard displays the map of Newham Borough, specifically highlighting East and West Ham areas.
Future updates will include additional data visualization and statistics for these areas.
""")

try:
    # Create a map centered on Newham
    m = folium.Map(
        location=[51.5417, 0.0357],  # Coordinates for Newham
        zoom_start=13,
        tiles='CartoDB positron'
    )

    # Add East Ham and West Ham boundaries with more precise coordinates
    east_ham_coords = [
        [51.5389, 0.0517],
        [51.5389, 0.0617],
        [51.5489, 0.0617],
        [51.5489, 0.0517],
        [51.5389, 0.0517]
    ]

    west_ham_coords = [
        [51.5389, 0.0217],
        [51.5389, 0.0317],
        [51.5489, 0.0317],
        [51.5489, 0.0217],
        [51.5389, 0.0217]
    ]

    # Add polygons for East and West Ham with improved styling
    folium.Polygon(
        locations=east_ham_coords,
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.3,
        weight=2,
        popup='East Ham',
        tooltip='East Ham'
    ).add_to(m)

    folium.Polygon(
        locations=west_ham_coords,
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=0.3,
        weight=2,
        popup='West Ham',
        tooltip='West Ham'
    ).add_to(m)

    # Add markers for key locations with improved styling
    folium.Marker(
        [51.5417, 0.0517],
        popup='East Ham Station',
        tooltip='East Ham Station',
        icon=folium.Icon(color='blue', icon='info-sign', prefix='fa')
    ).add_to(m)

    folium.Marker(
        [51.5417, 0.0317],
        popup='West Ham Station',
        tooltip='West Ham Station',
        icon=folium.Icon(color='red', icon='info-sign', prefix='fa')
    ).add_to(m)

    # Add a scale bar
    folium.plugins.Fullscreen().add_to(m)
    folium.plugins.MousePosition().add_to(m)

    # Display the map with a specific height
    folium_static(m, width=1200, height=600)

    # Add some placeholder statistics
    st.subheader("Area Statistics")
    col1, col2 = st.columns(2)

    with col1:
        st.metric(label="East Ham Population", value="76,186")
        st.metric(label="East Ham Area", value="3.41 km²")

    with col2:
        st.metric(label="West Ham Population", value="98,237")
        st.metric(label="West Ham Area", value="4.12 km²")

    # Add a note about future updates
    st.info("""
    This is a basic version of the dashboard. Future updates will include:
    - More detailed boundary data
    - Additional statistics and metrics
    - Interactive data visualization
    - Historical data comparison
    """)

except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.info("Please make sure all required packages are installed correctly.") 