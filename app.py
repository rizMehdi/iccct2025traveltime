import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium.plugins import AntPath
from geopy.distance import geodesic

# Sample venue coordinates
venues = {
    "Mumbai": (19.0760, 72.8777),
    "Delhi": (28.6139, 77.2090),
    "Kolkata": (22.5726, 88.3639),
    "Chennai": (13.0827, 80.2707),
}

# Sample travel data (City A, City B, Travel Time in hours)
travel_data = [
    ("Mumbai", "Delhi", 2.5),
    ("Delhi", "Kolkata", 2.0),
    ("Kolkata", "Chennai", 2.5),
    ("Chennai", "Mumbai", 1.5),
]

# Streamlit UI
st.title("🏏 Cricket Team Travel Visualization")
st.write("Animated travel paths between match venues with estimated travel time.")

# Create Folium Map
m = folium.Map(location=[22, 80], zoom_start=5, tiles="cartodbpositron")

# Add markers for venues
for city, (lat, lon) in venues.items():
    folium.Marker(
        [lat, lon], 
        popup=f"<b>{city}</b>", 
        tooltip=city, 
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

# Add animated & curved travel routes
for start, end, time in travel_data:
    start_coords = venues[start]
    end_coords = venues[end]

    # Compute a midpoint for the curve
    midpoint = [
        (start_coords[0] + end_coords[0]) / 2 + 2,  # Offset latitude slightly for curve
        (start_coords[1] + end_coords[1]) / 2 - 2   # Offset longitude slightly for curve
    ]

    # Animated AntPath with a curve
    AntPath(
        locations=[start_coords, midpoint, end_coords], 
        dash_array=[10, 20], 
        weight=3, 
        color="red", 
        delay=800
    ).add_to(m)

    # Add travel time as a popup at midpoint
    folium.Marker(
        midpoint,
        popup=f"{time} hrs",
        icon=folium.DivIcon(html=f"<b>{time}h</b>")
    ).add_to(m)

# Display the interactive map
folium_static(m)
