import streamlit as st
import folium
from streamlit_folium import folium_static
from folium.plugins import AntPath

# Match venues and their coordinates
venues = {
    "National Stadium, Karachi": (24.8924, 67.0652),
    "Gaddafi Stadium, Lahore": (31.5204, 74.3587),
    "Rawalpindi Cricket Stadium, Rawalpindi": (33.6361, 73.0486),
    "Dubai International Cricket Stadium, Dubai": (25.276987, 55.296249),
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

# Extract unique teams
teams = sorted(set([team for match in matches for team in [match[1], match[3]]]))

# Sidebar for team selection
selected_team = st.sidebar.selectbox("Select a team to view travel route:", ["All Teams"] + teams)

# Streamlit UI
st.title("🏏 Cricket Tournament Travel & Match Visualization")
st.write(f"Showing travel path for **{selected_team}**.")

# Center the map
m = folium.Map(location=[28, 69], zoom_start=5, tiles="cartodbpositron")

# Travel route sequence for selected team
travel_routes = []
prev_venue = None

# Add match details and connect travel paths
for match in matches:
    date, team1, score1, team2, score2, result, venue = match
    lat, lon = venues[venue]

    # Filter matches based on selection
    if selected_team != "All Teams" and selected_team not in [team1, team2]:
        continue

    # Assign color based on match result
    if "won" in result:
        color = "green" if team1 in result else "red"
    else:
        color = "gray"

    # Add match details
    folium.Marker(
        [lat, lon],
        popup=f"<b>{date}</b><br>{team1} {score1} vs {team2} {score2}<br><b>{result}</b>",
        tooltip=f"{date}: {team1} vs {team2}",
        icon=folium.Icon(color=color),
    ).add_to(m)

    # Store travel route
    if prev_venue:
        travel_routes.append((venues[prev_venue], (lat, lon)))

    prev_venue = venue

# Add animated travel paths
for (start, end) in travel_routes:
    AntPath(
        locations=[start, end],
        dash_array=[10, 20],
        weight=3,
        color="blue",
        delay=800,
    ).add_to(m)

# Display interactive map
folium_static(m)