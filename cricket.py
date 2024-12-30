import streamlit as st
import requests
import random
import toml
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Fetching data from CricAPI
config = toml.load('config.toml')
API_KEY = config['cricapi']['api_key']  # Replace with your actual API key
BASE_URL = "https://cricapi.com/api/matches?apikey=<API_KEY>"

def fetch_teams():
    url = f"{BASE_URL}teams?apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data['status'] == 'success':
        return [team['name'] for team in data['teams']]
    else:
        return []

def fetch_player_stats(team_name):
    url = f"{BASE_URL}players?apikey={API_KEY}&team={team_name}"
    response = requests.get(url)
    data = response.json()
    if data['status'] == 'success':
        return data['players']
    else:
        return []

# Function to simulate a cricket match
def simulate_match(team1, team2, match_format):
    # Fetch players for both teams
    players1 = fetch_player_stats(team1)
    players2 = fetch_player_stats(team2)
    
    # Here, we'll use random selection for simplicity
    # In a real scenario, we would use player stats to simulate match outcome
    score1 = random.randint(150, 350)  # Simulated score for Team 1
    score2 = random.randint(150, 350)  # Simulated score for Team 2

    # Determine winner based on score
    if score1 > score2:
        winner = team1
    elif score2 > score1:
        winner = team2
    else:
        winner = "Draw"
    
    # Simulate result in a basic format
    match_result = {
        'team1': team1,
        'team2': team2,
        'team1_score': score1,
        'team2_score': score2,
        'winner': winner
    }
    return match_result

# Create Streamlit user interface
def main():
    st.title("Cricket Match Simulator")
    
    # Choose teams and match format
    teams = fetch_teams()
    team1 = st.selectbox("Select Team 1", teams)
    team2 = st.selectbox("Select Team 2", teams)
    match_format = st.selectbox("Match Format", ["T20", "ODI", "Test"])
    
    # Simulate match button
    if st.button("Simulate Match"):
        result = simulate_match(team1, team2, match_format)
        st.write(f"**Match Result:**")
        st.write(f"{result['team1']} vs {result['team2']}")
        st.write(f"{result['team1']} Score: {result['team1_score']}")
        st.write(f"{result['team2']} Score: {result['team2_score']}")
        st.write(f"**Winner:** {result['winner']}")

# Run the app
if __name__ == "__main__":
    main()
