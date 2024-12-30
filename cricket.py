import streamlit as st
import pyCricbuzz
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Initialize the Cricbuzz API
c = pyCricbuzz.Cricbuzz()

# Function to fetch player data from Cricbuzz
def fetch_player_data():
    # Fetching players' data (example: batsmen's average, bowling average)
    # You can use specific player stats based on team/season or global
    # This will be a placeholder; you can customize based on available data
    player_stats = {
        "Player1": {"batting_average": 30, "bowling_average": 25},
        "Player2": {"batting_average": 35, "bowling_average": 28},
        "Player3": {"batting_average": 22, "bowling_average": 35},
        "Player4": {"batting_average": 40, "bowling_average": 22},
        "Player5": {"batting_average": 15, "bowling_average": 40},
    }
    return player_stats

# Simulate match based on input data
def simulate_match(team1, team2, format):
    # Fetch player data
    team1_data = fetch_player_data()
    team2_data = fetch_player_data()

    # Feature Engineering: Calculate average batting and bowling stats
    team1_batting_avg = sum([player["batting_average"] for player in team1_data.values()]) / len(team1_data)
    team1_bowling_avg = sum([player["bowling_average"] for player in team1_data.values()]) / len(team1_data)

    team2_batting_avg = sum([player["batting_average"] for player in team2_data.values()]) / len(team2_data)
    team2_bowling_avg = sum([player["bowling_average"] for player in team2_data.values()]) / len(team2_data)

    # Feature set: [batting_avg, bowling_avg, format (encoded)]
    format_encoding = {"T20": 0, "ODI": 1, "Test": 2}
    features = [[team1_batting_avg, team1_bowling_avg, format_encoding[format]],
                [team2_batting_avg, team2_bowling_avg, format_encoding[format]]]

    # Dummy Random Forest Model - Placeholder for an actual trained model
    model = RandomForestClassifier()
    
    # Normally, you would train your model with historical match data
    # Here, we simulate with random data just for illustration
    data = [[35, 28, 0], [30, 26, 1], [25, 29, 2], [32, 27, 0]]  # Example feature data
    labels = [1, 0, 1, 0]  # 1 = Team1 wins, 0 = Team2 wins
    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2)
    
    model.fit(X_train, y_train)

    # Predict the outcome (team1 vs team2 win prediction)
    result = model.predict(features)

    if result[0] == 1:
        return f"{team1} wins the match!"
    else:
        return f"{team2} wins the match!"

# Streamlit UI
st.title("Cricket Match Simulator")

# User inputs
team1 = st.selectbox("Choose Team 1", ["India", "Australia", "England", "Pakistan", "South Africa", "New Zealand"])
team2 = st.selectbox("Choose Team 2", ["India", "Australia", "England", "Pakistan", "South Africa", "New Zealand"])
format = st.radio("Choose Match Format", ("T20", "ODI", "Test"))

# Run the simulation on button click
if st.button("Simulate Match"):
    result = simulate_match(team1, team2, format)
    st.write(result)  # Display the match simulation results
