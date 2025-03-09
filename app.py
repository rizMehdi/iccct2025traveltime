import streamlit as st
import folium
from streamlit_folium import folium_static
import math
from folium.plugins import AntPath, PolyLineTextPath
import time

st.sidebar.title("🏏 ICC Champions Trophy 2025 - Team Travel")

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
    ("4 Mar", "Australia", "264 (49.3)", "India", "267/6 (48.1)", "India won by 4 wickets", "Dubai International Cricket Stadium, Dubai"),
    ("5 Mar", "New Zealand", "362/6 (50)", "South Africa", "312/9 (50)", "New Zealand won by 50 runs", "Gaddafi Stadium, Lahore"),
    ("9 Mar", "New Zealand", "-", "India", "-", "Being Played", "Dubai International Cricket Stadium, Dubai"),
]

# Assign colors to each team (as close as possible to their cricket team colors)
team_colors = {
    "New Zealand": "black",
    "Pakistan": "green",
    "Bangladesh": "darkgreen",
    "India": "blue",
    "South Africa": "darkred",  # Updated to a less bright color
    "England": "darkblue",
    "Australia": "gold",
    "Afghanistan": "red",
}

# Extract unique teams
teams = sorted(set([team for match in matches for team in [match[1], match[3]]]))
option_map = {team: team for team in teams}

# Sidebar for team selection using pills widget
team_option = st.sidebar.pills(
    "Select a team to see its travel and matches",
    options=option_map.keys(),
    format_func=lambda option: option_map[option],
    selection_mode="single",
    default="Afghanistan"  # Set Afghanistan as the default selected team
)

# Filter matches for the selected team
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

# Function to calculate travel routes for all teams
def calculate_all_teams_travel(matches):
    travel_routes = []
    for team in teams:
        prev_venue = None
        for match in matches:
            date, team1, score1, team2, score2, result, venue = match
            if team == team1 or team == team2:
                lat, lon = venues[venue][1]
                if prev_venue:
                    prev_lat, prev_lon = venues[prev_venue][1]
                    travel_routes.append((venues[prev_venue][1], (lat, lon), team_colors[team]))
                prev_venue = venue
    return travel_routes

# Show travel kilometers below the dropdown
if team_option != "All Teams":
    total_distance, travel_details = calculate_total_distance(filtered_matches, team_option)
    st.sidebar.write(f"✈️ **Total Travel Distance for {team_option}: {total_distance:.2f} km**")
#     for detail in travel_details:
#         st.sidebar.write(detail)
else:
    travel_routes = calculate_all_teams_travel(matches)
    st.sidebar.write("✈️ **Travel Distance for All Teams**: Calculated individually for each team")

# Function to determine match result emoji
def get_result_emoji(result, team, team1, team2):
    if "won" in result:
        if team in result:
            return "🟢"  # Green circle for win
        else:
            return "🔴"  # Red circle for loss
    elif "No result" in result or "Match abandoned" in result:
        return "🔵"  # Blue circle for draw
    return ""

# Sidebar for Match List with separate expanders
with st.sidebar:
    if team_option == "All Teams":
        st.write("Select a team from above to see its matches and travel.")
    else:
        prev_venue = None
        for match in filtered_matches:
            date, team1, score1, team2, score2, result, venue = match
            city = venues[venue][0]  # Extract city name for the expander title
            opponent = team2 if team1 == team_option else team1
            
            # Display travel distance if not the first venue
            if prev_venue and prev_venue != venue:
                lat1, lon1 = venues[prev_venue][1]
                lat2, lon2 = venues[venue][1]
                distance = haversine(lat1, lon1, lat2, lon2)
                st.warning(f"✈️ Travel from {venues[prev_venue][0]} to {venues[venue][0]}: {distance:.2f} km.")
            
            result_emoji = get_result_emoji(result, team_option, team1, team2)
            with st.expander(f"{result_emoji} {date}, {city}: {team1} vs {team2}"):
                st.write(f"🏟 **{venue}**")
                if "Match abandoned" not in result and "No result" not in result:
                    st.write(f"🏏 {team1}: {score1}, {team2}: {score2}")
                st.write(f"🏆 {result}")
            
            prev_venue = venue

# Streamlit UI
st.write(f"Showing travel paths for {team_option if team_option != 'All Teams' else 'all teams'}")

# Keep map centered
m = folium.Map(location=[28, 69], zoom_start=5, tiles="https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png", attr='Map tiles by CartoDB, under CC BY 3.0. Data by OpenStreetMap, under ODbL.', scrollWheelZoom=False, zoomControl=False)

# Function to add offset to marker labels
def add_offset(lat, lon, offset=0.005):
    return lat + offset, lon + offset

# Travel route sequence for selected teams
travel_routes = []
if team_option == "All Teams":
    travel_routes = calculate_all_teams_travel(filtered_matches)
else:
    prev_venue = None
    match_number = 1
    for match in filtered_matches:
        date, team1, score1, team2, score2, result, venue = match
        lat, lon = venues[venue][1]

        # Choose team color of the team that is changing venue
        if prev_venue:
            if team1 == team_option:
                team_color = team_colors.get(team1, "gray")
            else:
                team_color = team_colors.get(team2, "gray")
        else:
            team_color = team_colors.get(team1 if team1 == team_option else team2, "gray")

        # Add match details with match number using DivIcon
        city = venues[venue][0]
        offset_lat, offset_lon = add_offset(lat, lon)
        folium.Marker(
            location=[offset_lat, offset_lon],
            popup=f"<b>Match {match_number}</b><br>{date}<br>{team1} {score1} vs {team2} {score2}<br><b>{result}</b>",
            icon=folium.DivIcon(html=f"""<div style="font-family: verdana; color: black; font-weight: bold">{city}</div>""")
        ).add_to(m)

        # Store travel route (for team-colored lines)
        if prev_venue:
            travel_routes.append((venues[prev_venue][1], (lat, lon), team_color))

        prev_venue = venue
        match_number += 1

# Function to add plane-like dashed line with direction in tube map style
def add_plane_line(start, end, color, offset=0):
    lat1, lon1 = start
    lat2, lon2 = end

    # Offset the coordinates to create parallel lines if overlapping
    if offset != 0:
        lat1 += offset / 100
        lon1 += offset / 100
        lat2 += offset / 100
        lon2 += offset / 100

    # Create an animated polyline with dashed lines representing planes
    plane_line = AntPath(
        locations=[[lat1, lon1], [lat2, lon2]],
        color=color,
        weight=10,  # Thicker line (3x the current)
        opacity=0.5,  # Translucent lines
        dash_array=[10, 20],  # Dash pattern
        delay=1000  # Animation delay
    ).add_to(m)

# Add travel routes to the map with offsets for parallel lines
offset = 0
for start, end, color in travel_routes:
    add_plane_line(start, end, color, offset)
    offset += 0.01  # Increment offset for parallel lines

# Display the map
folium_static(m)