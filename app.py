import streamlit as st
import folium
from streamlit_folium import folium_static
import math
from folium.plugins import AntPath

# Match venues and their coordinates (city only for the expander titles)
venues = {
    "National Stadium, Karachi": ("Karachi", (24.8924, 67.0652)),
    "Gaddafi Stadium, Lahore": ("Lahore", (31.5204, 74.3587)),
    "Rawalpindi Cricket Stadium, Rawalpindi": ("Rawalpindi", (33.6361, 73.0486)),
    "Dubai International Cricket Stadium, Dubai": ("Dubai", (25.276987, 55.296249)),
}

# Match data (Date, Team1, Score1, Team2, Score2, Result, Venue)
matches = [
    ("19 Feb", "New Zealand", "320/5 (50)", "Pakistan", "260 (47.2)", "New Zealand won by 60 runs", "National Stadium, Karachi"),
    ("20 Feb", "Bangladesh", "228 (49.4)", "India", "231/4 (46.3)", "India won by 6 wickets", "Dubai International Cricket Stadium, Dubai"),
    ("21 Feb", "South Africa", "315/6 (50)", "Afghanistan", "208 (43.3)", "South Africa won by 107 runs", "National Stadium, Karachi"),
    ("22 Feb", "England", "351/8 (50)", "Australia", "356/5 (47.3)", "Australia won by 5 wickets", "Gaddafi Stadium, Lahore"),
    ("23 Feb", "Pakistan", "241 (49.4)", "India", "244/4 (42.3)", "India won by 6 wickets", "Dubai International Cricket Stadium, Dubai"),
    ("24 Feb", "Bangladesh", "236/9 (50)", "New Zealand", "240/5 (46.1)", "New Zealand won by 5 wickets", "Rawalpindi Cricket Stadium, Rawalpindi"),
    ("25 Feb", "Australia", "-", "South Africa", "-", "Match abandoned", "Rawalpindi Cricket Stadium, Rawalpindi"),
    ("26 Feb", "Afghanistan", "325/7 (50)", "England", "317 (49.5)", "Afghanistan won by 8 runs", "Gaddafi Stadium, Lahore"),
    ("27 Feb", "Pakistan", "-", "Bangladesh", "-", "Match abandoned", "Rawalpindi Cricket Stadium, Rawalpindi"),
    ("28 Feb", "Afghanistan", "273 (50)", "Australia", "109/1 (12.5)", "No result", "Gaddafi Stadium, Lahore"),
    ("1 Mar", "England", "179 (38.2)", "South Africa", "181/3 (29.1)", "South Africa won by 7 wickets", "National Stadium, Karachi"),
    ("2 Mar", "India", "249/9 (50)", "New Zealand", "205 (45.3)", "India won by 44 runs", "Dubai International Cricket Stadium, Dubai"),
]

# Assign colors to each team (Modified Australia to yellow + green)
team_colors = {
    "New Zealand": ["black", "white"],
    "Pakistan": ["green", "white"],
    "Bangladesh": ["green", "red"],
    "India": ["blue", "orange"],
    "South Africa": ["green", "black"],
    "England": ["red", "white"],
    "Australia": ["yellow", "green"],  # Updated to yellow and green
    "Afghanistan": ["red"],
}

# Extract unique teams
teams = sorted(set([team for match in matches for team in [match[1], match[3]]]))

# Sidebar for team selection using dropdown (selectbox)
team_option = st.sidebar.selectbox("Select Team", ["All Teams"] + teams)

# Filter matches for the selected team
if team_option == "All Teams":
    filtered_matches = matches
else:
    filtered_matches = [match for match in matches if team_option in [match[1], match[3]]]

# Function to calculate distance between two points (Haversine formula)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c  # Distance in km

# Calculate total travel distance for the selected team
def calculate_total_distance(matches, team):
    total_distance = 0
    prev_venue = None
    travel_details = []
    for match in matches:
        date, team1, score1, team2, score2, result, venue = match
        if team == team1 or team == team2:
            lat, lon = venues[venue][1]
            if prev_venue:
                prev_lat, prev_lon = venues[prev_venue][1]
                distance = haversine(prev_lat, prev_lon, lat, lon)
                travel_details.append(f"Travel from {venues[prev_venue][0]} to {venues[venue][0]}: {distance:.2f} km.")
                total_distance += distance
            prev_venue = venue
    return total_distance, travel_details

# Show travel kilometers below the dropdown
if team_option != "All Teams":
    total_distance, travel_details = calculate_total_distance(filtered_matches, team_option)
    st.sidebar.write(f"✈️ **Total Travel Distance for {team_option}: {total_distance:.2f} km**")
    for detail in travel_details:
        st.sidebar.write(detail)
else:
    st.sidebar.write("✈️ **Travel Distance for All Teams**: Calculated individually for each team")

# Sidebar for Match List with separate expanders
with st.sidebar:
    for match in filtered_matches:
        date, team1, score1, team2, score2, result, venue = match
        city = venues[venue][0]  # Extract city name for the expander title
        opponent = team2 if team1 == team_option or team_option == "All Teams" else team1
        
        with st.expander(f"{date}, {city}: {team1} vs {opponent}"):
            st.write(f"🏟 **{venue}**")
            st.write(f"🏏 {team1}: {score1}, {team2}: {score2}")
            st.write(f"🏆 {result}")

# Streamlit UI
st.title("🏏 Cricket Tournament Travel & Match Visualization")
st.write(f"Showing travel paths for {team_option if team_option != 'All Teams' else 'all teams'}")

# Keep map centered
m = folium.Map(location=[28, 69], zoom_start=5, tiles="cartodbpositron")

# Travel route sequence for selected teams
travel_routes = []
prev_venue = None

# Add match details and connect travel paths
for match in filtered_matches:
    date, team1, score1, team2, score2, result, venue = match
    lat, lon = venues[venue][1]

    # Choose team color(s)
    team_color = team_colors.get(team1 if team1 == team_option or team_option == "All Teams" else team2, ["gray"])

    # Add match details
    folium.Marker(
        [lat, lon],
        popup=f"<b>{date}</b><br>{team1} {score1} vs {team2} {score2}<br><b>{result}</b>",
        tooltip=f"{date}: {team1} vs {team2}",
        icon=folium.Icon(color=team_color[0]),
    ).add_to(m)

    # Store travel route (for team-colored lines)
    if prev_venue:
        travel_routes.append((venues[prev_venue][1], (lat, lon), team_color))

    prev_venue = venue

# Function to add plane-like dashed line
def add_plane_line(start, end, color):
    lat1, lon1 = start
    lat2, lon2 = end

    # Create a polyline with dashed lines representing planes
    plane_line = folium.PolyLine(
        [[lat1, lon1], [lat2, lon2]],
        weight=3,
        color=color,
        dash_array="5, 10",  # Dash pattern (less frequent planes)
    ).add_to(m)

# Add plane-like travel paths
for (start, end, colors) in travel_routes:
    for color in colors:
        add_plane_line(start, end, color)

# Display interactive map
folium_static(m)