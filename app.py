import streamlit as st
import folium
from streamlit_folium import folium_static
from folium.plugins import AntPath
import numpy as np
from scipy.interpolate import interp1d

# Venue coordinates (Pakistan & Dubai)
venues = {
    "National Stadium, Karachi": (24.8924, 67.0652),
    "Gaddafi Stadium, Lahore": (31.5204, 74.3587),
    "Rawalpindi Cricket Stadium, Rawalpindi": (33.6361, 73.0486),
    "Dubai International Cricket Stadium, Dubai": (25.276987, 55.296249),
}

# Travel data (Start, End, Travel Time in hours)
travel_data = [
    ("National Stadium, Karachi", "Gaddafi Stadium, Lahore", 1.5),
    ("Gaddafi Stadium, Lahore", "Rawalpindi Cricket Stadium, Rawalpindi", 0.5),
    ("Rawalpindi Cricket Stadium, Rawalpindi", "Dubai International Cricket Stadium, Dubai", 3.0),
    ("Dubai International Cricket Stadium, Dubai", "National Stadium, Karachi", 2.5),
]

# Streamlit UI
st.title("🏏 Cricket Team Travel Visualization")
st.write("Smooth curved travel paths between match venues in Pakistan & UAE.")

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

# Function to generate smooth Bezier curve between two points
def bezier_curve(start, end, control_offset=3, num_points=30):
    lat1, lon1 = start
    lat2, lon2 = end

    # Control point to create curvature (Offset for a nice curve)
    control_lat = (lat1 + lat2) / 2 + control_offset
    control_lon = (lon1 + lon2) / 2 - control_offset

    # Create parameterized values
    t = np.linspace(0, 1, num_points)
    
    # Compute Bezier curve points
    curve_lats = (1 - t) ** 2 * lat1 + 2 * (1 - t) * t * control_lat + t ** 2 * lat2
    curve_lons = (1 - t) ** 2 * lon1 + 2 * (1 - t) * t * control_lon + t ** 2 * lon2

    return list(zip(curve_lats, curve_lons))

# Add animated smooth travel paths
for start, end, time in travel_data:
    start_coords = venues[start]
    end_coords = venues[end]

    # Generate a smooth Bezier curve
    curve_path = bezier_curve(start_coords, end_coords)

    # Animated AntPath for movement
    AntPath(
        locations=curve_path, 
        dash_array=[10, 20], 
        weight=3, 
        color="red", 
        delay=800
    ).add_to(m)

    # Travel time popup at midpoint
    midpoint = curve_path[len(curve_path) // 2]
    folium.Marker(
        midpoint,
        popup=f"{time} hrs",
        icon=folium.DivIcon(html=f"<b>{time}h</b>")
    ).add_to(m)

# Display interactive map
folium_static(m)
