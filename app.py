import streamlit as st
import folium
from streamlit_folium import folium_static
from folium.plugins import AntPath

# Updated venue coordinates (Pakistan & Dubai)
venues = {
    "National Stadium, Karachi": (24.8924, 67.0652),
    "Gaddafi Stadium, Lahore": (31.5204, 74.3587),
    "Rawalpindi Cricket Stadium, Rawalpindi": (33.6361, 73.0486),
    "Dubai International Cricket Stadium, Dubai": (25.276987, 55.296249),
}

# Travel data: (City A, City B, Travel Time in hours)
travel_data = [
    ("National Stadium, Karachi", "Gaddafi Stadium, Lahore", 1.5),
    ("Gaddafi Stadium, Lahore", "Rawalpindi Cricket Stadium, Rawalpindi", 0.5),
    ("Rawalpindi Cricket Stadium, Rawalpindi", "Dubai International Cricket Stadium, Dubai", 3.0),
    ("Dubai International Cricket Stadium, Dubai", "National Stadium, Karachi", 2.5),
]

# Streamlit UI
st.title("🏏 Cricket Team Travel Visualization")
st.write("Animated travel paths between match venues in Pakistan & UAE.")

# Center the map around Pakistan & Dubai
m = folium.Map(location=[28, 69], zoom_start=5, tiles="cartodbpositron")

# Add venue markers
for city, (lat, lon) in venues.items():
    folium.Marker(
        [lat, lon], 
        popup=f"<b>{city}</b>", 
        tooltip=city, 
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

# Add animated curved travel routes
for start, end, time in travel_data:
    start_coords = venues[start]
    end_coords = venues[end]

    # Compute a midpoint for the curve
    midpoint = [
        (start_coords[0] + end_coords[0]) / 2 + 1,  # Offset latitude for curve effect
        (start_coords[1] + end_coords[1]) / 2 - 1   # Offset longitude for curve effect
    ]

    # Animated AntPath with a curve
    AntPath(
        locations=[start_coords, midpoint, end_coords], 
        dash_array=[10, 20], 
        weight=3, 
        color="red", 
        delay=800
    ).add_to(m)

    # Travel time popup at midpoint
    folium.Marker(
        midpoint,
        popup=f"{time} hrs",
        icon=folium.DivIcon(html=f"<b>{time}h</b>")
    ).add_to(m)

# Display interactive map
folium_static(m)
