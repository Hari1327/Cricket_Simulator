import streamlit as st
import pandas as pd

# Load player data
@st.cache_data
def load_player_data():
    df = pd.read_csv("Batters.csv")
    df['Role'] = df.apply(lambda row: 
        'Batter' if row['Batter'] == 1 else
        'Bowler' if row['Bowler'] == 1 else
        'Allrounder' if row['AllRounder'] == 1 else
        'WicketKeeper' if row['WicketKeeper'] == 1 else
        'Spinner', axis=1)
    return df[['Player', 'Role']]

# Initialize session state
if 'team1_players' not in st.session_state:
    st.session_state.team1_players = []
if 'team2_players' not in st.session_state:
    st.session_state.team2_players = []

# Load player data
players_df = load_player_data()

st.title("Cricket Team Selector 🏏")

def player_card(player, role):
    """Create a simple player card with remove button"""
    return f"""
    <div style='border: 1px solid #e0e0e0; border-radius: 5px; padding: 10px; margin: 5px 0;
                display: flex; justify-content: space-between; align-items: center;'>
        <div>
            <strong>{player}</strong><br>
            <span style='color: #666; font-size: 0.9em;'>{role}</span>
        </div>
    </div>
    """

# Create two columns for teams
col1, col2 = st.columns(2)

with col1:
    st.header("Team 1")
    
    # Get available players for Team 1
    available_team1 = [p for p in players_df['Player'] 
                      if p not in st.session_state.team1_players + st.session_state.team2_players]
    
    # Player selection
    selected_player_1 = st.selectbox("Select Team 1 Players", available_team1)
    
    # Add button
    if st.button("Add to Team 1"):
        st.session_state.team1_players.append(selected_player_1)
    
    # Selected players with remove buttons
    st.subheader("Selected Players")
    players_to_remove = []
    for idx, player in enumerate(st.session_state.team1_players):
        role = players_df[players_df['Player'] == player]['Role'].values[0]
        st.markdown(player_card(player, role), unsafe_allow_html=True)
        
        # Remove button
        if st.button(f"Remove {player}", key=f"remove1_{player}"):
            players_to_remove.append(player)
    
    # Update team after removal
    for player in players_to_remove:
        st.session_state.team1_players.remove(player)

with col2:
    st.header("Team 2")
    
    # Get available players for Team 2
    available_team2 = [p for p in players_df['Player'] 
                      if p not in st.session_state.team2_players + st.session_state.team1_players]
    
    # Player selection
    selected_player_2 = st.selectbox("Select Team 2 Players", available_team2)
    
    # Add button
    if st.button("Add to Team 2"):
        st.session_state.team2_players.append(selected_player_2)
    
    # Selected players with remove buttons
    st.subheader("Selected Players")
    players_to_remove = []
    for idx, player in enumerate(st.session_state.team2_players):
        role = players_df[players_df['Player'] == player]['Role'].values[0]
        st.markdown(player_card(player, role), unsafe_allow_html=True)
        
        # Remove button
        if st.button(f"Remove {player}", key=f"remove2_{player}"):
            players_to_remove.append(player)
    
    # Update team after removal
    for player in players_to_remove:
        st.session_state.team2_players.remove(player)

# Simulation button
if st.button("Simulate Match"):
    if len(st.session_state.team1_players) > 0 and len(st.session_state.team2_players) > 0:
        st.success("Match simulation started!")
    else:
        st.error("Please select players for both teams first!")
