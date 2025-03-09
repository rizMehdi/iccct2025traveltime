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

# Assign colors to each team (Modified to include two-color schemes for some teams)
team_colors = {
    "New Zealand": ["black", "white"],
    "Pakistan": ["green", "white"],
    "Bangladesh": ["green", "red"],
    "India": ["blue", "orange"],
    "South Africa": ["green", "black"],
    "England": ["red", "white"],
    "Australia": ["yellow"],
    "Afghanistan": ["red"],
}

# Extract unique teams
teams = sorted(set([team for match in matches for team in [match[1], match[3]]]))

# Sidebar for team selection
selected_team = st.sidebar.selectbox("Select a team to view travel route:", ["All Teams"] + teams)

# Filter matches for the selected team
filtered_matches = [match for match in matches if selected_team in [match[1], match[3]]] if selected_team != "All Teams" else matches

# Sidebar Match List
st.sidebar.write(f"### Matches for {selected_team}" if selected_team != "All Teams" else "### All Matches")
for match in filtered_matches:
    date, team1, score1, team2, score2, result, venue = match
    opponent = team2 if team1 == selected_team else team1
    st.sidebar.write(f"📅 **{date}**: {selected_team} vs {opponent}\n- 🏟 **Venue:** {venue}\n- 🏆 **Result:** {result}")

# Streamlit UI
st.title("🏏 Cricket Tournament Travel & Match Visualization")
st.write(f"Showing travel path for **{selected_team}**.")

# Keep map centered
m = folium.Map(location=[28, 69], zoom_start=5, tiles="cartodbpositron")

# Travel route sequence for selected team
travel_routes = []
prev_venue = None

# Add match details and connect travel paths
for match in filtered_matches:
    date, team1, score1, team2, score2, result, venue = match
    lat, lon = venues[venue]

    # Choose team color(s)
    team_color = team_colors.get(team1 if team1 in result else team2, ["gray"])

    # Add match details
    folium.Marker(
        [lat, lon],
        popup=f"<b>{date}</b><br>{team1} {score1} vs {team2} {score2}<br><b>{result}</b>",
        tooltip=f"{date}: {team1} vs {team2}",
        icon=folium.Icon(color=team_color[0]),
    ).add_to(m)

    # Store travel route (for team-colored lines)
    if prev_venue:
        travel_routes.append((venues[prev_venue], (lat, lon), team_color))

    prev_venue = venue

# Add animated travel paths with team colors
for (start, end, colors) in travel_routes:
    for i, color in enumerate(colors):
        AntPath(
            locations=[start, end],
            dash_array=[10, 20],
            weight=3,
            color=color,
            delay=800 + (i * 200),  # Slight delay for each color transition
        ).add_to(m)

# Display interactive map
folium_static(m)