import streamlit as st
import folium
from streamlit_folium import folium_static
import geopandas as gpd
import pandas as pd
import requests
import json

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

    # Load ward boundaries for Newham
    # Using London Data Store ward boundaries
    url = "https://data.london.gov.uk/download/statistical-gis-boundary-files-london/9ba8c833-6370-4b11-abdc-314aa020d5e0/London-wards-2018_ESRI.zip"
    
    # Download and read the GeoJSON data
    @st.cache_data
    def load_ward_boundaries():
        try:
            # Read the GeoJSON file
            gdf = gpd.read_file("https://raw.githubusercontent.com/mingda/LLDC_EPC/main/newham_wards.geojson")
            return gdf
        except Exception as e:
            st.error(f"Error loading ward boundaries: {str(e)}")
            return None

    # Load the ward boundaries
    wards_gdf = load_ward_boundaries()
    
    if wards_gdf is not None:
        # Filter for East Ham and West Ham wards
        east_ham_ward = wards_gdf[wards_gdf['NAME'].str.contains('East Ham', case=False, na=False)]
        west_ham_ward = wards_gdf[wards_gdf['NAME'].str.contains('West Ham', case=False, na=False)]

        # Add East Ham ward to map
        if not east_ham_ward.empty:
            folium.GeoJson(
                east_ham_ward,
                style_function=lambda x: {
                    'fillColor': 'blue',
                    'color': 'blue',
                    'fillOpacity': 0.3,
                    'weight': 2
                },
                tooltip=folium.GeoJsonTooltip(
                    fields=['NAME'],
                    aliases=['Ward:'],
                    style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
                )
            ).add_to(m)

        # Add West Ham ward to map
        if not west_ham_ward.empty:
            folium.GeoJson(
                west_ham_ward,
                style_function=lambda x: {
                    'fillColor': 'red',
                    'color': 'red',
                    'fillOpacity': 0.3,
                    'weight': 2
                },
                tooltip=folium.GeoJsonTooltip(
                    fields=['NAME'],
                    aliases=['Ward:'],
                    style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
                )
            ).add_to(m)

    # Add markers for key locations
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

    # Add map controls
    folium.plugins.Fullscreen().add_to(m)
    folium.plugins.MousePosition().add_to(m)
    folium.plugins.MiniMap().add_to(m)

    # Display the map
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
    - Additional statistics and metrics
    - Interactive data visualization
    - Historical data comparison
    - More detailed ward information
    """)

except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.info("Please make sure all required packages are installed correctly.") 