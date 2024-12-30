import streamlit as st
import pyCricbuzz
import torch
import numpy as np

# Initialize PyCricbuzz Client
def get_player_stats(team_name):
    client = pyCricbuzz.PycBuzzClient()
    
    # Fetch the current series (you can modify to use specific series or matches)
    matches = client.matches()
    # Get ongoing match details (if any)
    if matches:
        match_id = matches[0]['id']  # Use the first ongoing match
        match_details = client.match_details(match_id)
        
        # Filter players for the requested team
        players = []
        for player in match_details['players']:
            if team_name.lower() in player['team'].lower():
                players.append({
                    'name': player['name'],
                    'bat_avg': player['batting_avg'],
                    'bowl_avg': player.get('bowling_avg', 0),  # Handle cases where bowling avg is missing
                    'team': player['team']
                })
        return players
    return []

# Dummy Model for Simulation (Replace with actual deep learning model)
class CricketMatchSimulator(torch.nn.Module):
    def __init__(self):
        super(CricketMatchSimulator, self).__init__()
        self.fc = torch.nn.Linear(10, 2)  # Example structure

    def forward(self, x):
        return self.fc(x)

# Simulate Match Function
def simulate_innings(model, team, match_format, max_overs):
    innings = {
        "total_runs": 0,
        "wickets": 0,
        "overs": [],
        "players": [{"name": p["name"], "runs": 0, "balls": 0, "out": False} for p in team]
    }

    for over in range(max_overs):
        if innings["wickets"] == len(team):
            break  # All players are out

        # Prepare features for the model (you can adjust this based on your simulation logic)
        over_features = match_format + [innings["total_runs"], innings["wickets"]]
        team_features = [p["bat_avg"] for p in team]
        input_features = torch.tensor(over_features + team_features, dtype=torch.float32)

        # Predict runs and wicket probabilities
        prediction = model(input_features).detach().numpy()
        runs, wicket_prob = int(prediction[0]), prediction[1]

        # Update innings state
        innings["total_runs"] += runs
        if np.random.rand() < wicket_prob:  # Simulate wicket
            innings["wickets"] += 1
            player = innings["players"][innings["wickets"] - 1]
            player["out"] = True
            player["runs"] += runs

        innings["overs"].append({"over": over + 1, "runs": runs, "wickets": innings["wickets"]})

    return innings

def generate_scorecard(team_name, innings):
    st.write(f"**Scorecard for {team_name}**")
    st.write(f"**Total:** {innings['total_runs']}/{innings['wickets']}")
    st.write("**Player Contributions:**")
    for player in innings["players"]:
        status = "Out" if player["out"] else "Not Out"
        st.write(f"{player['name']}: {player['runs']} ({player['balls']} balls) - {status}")

# Encode match format to numerical values
def encode_match_format(format_choice):
    format_dict = {"T20": [1, 0, 0], "ODI": [0, 1, 0], "Test": [0, 0, 1]}
    return format_dict.get(format_choice, [0, 0, 0])

# Streamlit UI for Input
def app():
    st.title("Cricket Match Simulator")
    
    # Get user inputs for teams and format
    team_a = st.text_input("Enter Team A Name", "India")
    team_b = st.text_input("Enter Team B Name", "Australia")
    format_choice = st.selectbox("Select Match Format", ["T20", "ODI", "Test"])
    
    if st.button("Simulate Match"):
        # Fetch player data for each team using PyCricbuzz
        team_a_data = get_player_stats(team_a)
        team_b_data = get_player_stats(team_b)

        if not team_a_data or not team_b_data:
            st.write("Could not fetch player data. Please check team names or match status.")
            return
        
        # Encode match format
        match_format_encoded = encode_match_format(format_choice)
        
        # Set max overs based on match format
        max_overs = 20 if format_choice == "T20" else 50 if format_choice == "ODI" else 90
        
        # Load model (replace with your trained model)
        model = CricketMatchSimulator()
        
        # Simulate innings for both teams
        st.write(f"\n**{team_a} Batting:**")
        innings_a = simulate_innings(model, team_a_data, match_format_encoded, max_overs)
        generate_scorecard(team_a, innings_a)
        
        st.write(f"\n**{team_b} Batting:**")
        innings_b = simulate_innings(model, team_b_data, match_format_encoded, max_overs)
        generate_scorecard(team_b, innings_b)
        
        # Determine winner
        if innings_a["total_runs"] > innings_b["total_runs"]:
            st.write(f"\n**{team_a} wins by {innings_a['total_runs'] - innings_b['total_runs']} runs!**")
        elif innings_b["total_runs"] > innings_a["total_runs"]:
            st.write(f"\n**{team_b} wins by {10 - innings_b['wickets']} wickets!**")
        else:
            st.write("\n**Match Drawn!**")

if __name__ == "__main__":
    app()
