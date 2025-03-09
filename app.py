import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from geopy.distance import geodesic

# Sample data
venues = {
    "Mumbai": (19.0760, 72.8777),
    "Delhi": (28.6139, 77.2090),
    "Kolkata": (22.5726, 88.3639),
    "Chennai": (13.0827, 80.2707),
}

travel_data = [
    ("Mumbai", "Delhi", 2.5),  # Flight time in hours
    ("Delhi", "Kolkata", 2.0),
    ("Kolkata", "Chennai", 2.5),
    ("Chennai", "Mumbai", 1.5),
]

# Streamlit UI
st.title("Cricket Team Travel Time Visualization")

# Create a Folium map
m = folium.Map(location=[22, 80], zoom_start=5)

# Add markers
for city, (lat, lon) in venues.items():
    folium.Marker([lat, lon], popup=city, tooltip=city).add_to(m)

# Add travel routes
for start, end, time in travel_data:
    start_coords = venues[start]
    end_coords = venues[end]
    folium.PolyLine([start_coords, end_coords], color="blue", weight=2.5, opacity=0.7).add_to(m)
    midpoint = [(start_coords[0] + end_coords[0]) / 2, (start_coords[1] + end_coords[1]) / 2]
    folium.Marker(midpoint, popup=f"{time} hrs", icon=folium.DivIcon(html=f"<b>{time}h</b>")).add_to(m)

# Display map
folium_static(m)
