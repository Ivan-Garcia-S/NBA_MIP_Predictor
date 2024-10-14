import pandas as pd
import re
# Function to check if a value is a valid date (season)
def is_valid_season(season):
    return str(season).startswith('2')

def fill_missing_seasons(df, column_name):
    last_valid_season = None

    for i, row in df.iterrows():
        current_season = row[column_name]

        # If the season is valid, update the last valid season
        if is_valid_season(current_season):
            last_valid_season = current_season
        # If the season is not valid, populate with the last valid season
        elif last_valid_season:
            df.at[i, column_name] = last_valid_season

    return df

'''
def find_differential_of_stats(df):

    df["PTS_Differential"] = pd.NA
    df["REB_Differential"] = pd.NA
    df["AST_Differential"] = pd.NA

    # Dictionary to store differentials
    player_differentials = {}

    for i, row in df.iterrows():
        if(1 <= int(row["Rank"].replace("T", "")) <= 3):

            player_name = row["Player"]

            current_szn_file = row["Season"] + '-PerGame.csv'
            df_current = pd.read_csv(current_szn_file)

            years = row["Season"].split("-")
            prev_year = int(years[0]) - 1
            prev_year_second = int(years[0]) - 2000
            prev_year_second = "{:02d}".format(prev_year_second)

            prev_szn_file = str(prev_year) + "-" + str(prev_year_second) + '-PerGame.csv'
            df_prev = pd.read_csv(prev_szn_file)

            
            player_this_year = df_current.loc[df_current['Player'] == player_name]
            player_last_year = df_prev.loc[df_prev['Player'] == player_name]

            if not player_this_year.empty and not player_last_year.empty:
                pts_differential = player_this_year["PTS"].values[0] - player_last_year["PTS"].values[0]
                reb_differential = player_this_year["TRB"].values[0] - player_last_year["TRB"].values[0]
                ast_differential = player_this_year["AST"].values[0] - player_last_year["AST"].values[0]

                # Store the differentials in the dictionary
                player_differentials[player_name] = {
                    'PTS_Differential': pts_differential,
                    'REB_Differential': reb_differential,
                    'AST_Differential': ast_differential
                }


    for player_name, diffs in player_differentials.items():
        # Ensure the correct rows are updated
        df.loc[(df["Player"] == player_name) & (df["Rank"].between(1, 3)), 'PTS_Differential'] = diffs['PTS_Differential']
        df.loc[(df["Player"] == player_name) & (df["Rank"].between(1, 3)), 'REB_Differential'] = diffs['REB_Differential']
        df.loc[(df["Player"] == player_name) & (df["Rank"].between(1, 3)), 'AST_Differential'] = diffs['AST_Differential']


    return df
'''
def find_differential_of_stats(df):
    def clean_player_name(name):
        # Use regular expression to remove extra text starting with a slash
        return re.sub(r'\\.*$', '', name).strip()
    
    # Create new columns for the differentials
    df['PTS_Differential'] = pd.NA
    df['REB_Differential'] = pd.NA
    df['AST_Differential'] = pd.NA

    # Dictionary to store differentials
    player_differentials = {}
    lowest_games_prev = 82

    # Iterate over the DataFrame to collect player stats
    for i, row in df.iterrows():
        if 1 <= int(row["Rank"].replace("T", "")) <= 3:
            player_name = row["Player"]
            season = row["Season"]
            print(player_name)
            print(season)
            current_szn_file = row["Season"] + '-PerGame.csv'
            df_current = pd.read_csv(current_szn_file)

            years = row["Season"].split("-")
            prev_year = int(years[0]) - 1
            prev_year_second = int(years[0]) - 2000
            prev_year_second = "{:02d}".format(prev_year_second)

            prev_szn_file = str(prev_year) + "-" + str(prev_year_second) + '-PerGame.csv'
            df_prev = pd.read_csv(prev_szn_file)


            df_current['Player'] = df_current['Player'].apply(clean_player_name)
            df_prev['Player'] = df_prev['Player'].apply(clean_player_name)
            player_this_year = df_current.loc[df_current["Player"] == player_name]#df_current['Player'].apply(clean_player_name) == player_name]
            player_last_year = df_prev.loc[df_prev["Player"] == player_name]#df_prev['Player'].apply(clean_player_name) == player_name]
            print("Plauer this year=", player_this_year)

            if not player_this_year.empty and not player_last_year.empty:
                pts_differential = player_this_year["PTS"].values[0] - player_last_year["PTS"].values[0]
                reb_differential = player_this_year["TRB"].values[0] - player_last_year["TRB"].values[0]
                ast_differential = player_this_year["AST"].values[0] - player_last_year["AST"].values[0]
                
                games_prev = player_last_year["G"].values[0]
                lowest_games_prev = min(lowest_games_prev, games_prev)

                # Store the differentials in the dictionary
                if player_name in player_differentials:
                    player_differentials[player_name + "2"] = {
                        'PTS_Differential': pts_differential,
                        'REB_Differential': reb_differential,
                        'AST_Differential': ast_differential,
                        'Season': season
                        
                    }
                else:
                    player_differentials[player_name] = {
                        'PTS_Differential': pts_differential,
                        'REB_Differential': reb_differential,
                        'AST_Differential': ast_differential,
                        'Season': season
                    }
                
            else:
                print("EMPTY")

    # Update the DataFrame with the differentials
    for player_name, diffs in player_differentials.items():
        # Ensure the correct rows are updated
        mask = (df["Player"] == player_name.replace("2", "")) & (df["Season"] == player_differentials[player_name]["Season"])
        df.loc[mask, 'PTS_Differential'] = diffs['PTS_Differential']
        df.loc[mask, 'REB_Differential'] = diffs['REB_Differential']
        df.loc[mask, 'AST_Differential'] = diffs['AST_Differential']

    return df, lowest_games_prev

def get_previous_season(current_season):
    years = current_season.split('-')
    
    first_year = str(int(years[0]) - 1)
    second_year = '{:02d}'.format(int(years[1]) - 1)
    return first_year + '-' + second_year


def find_lowest_games_season_before(top_n_candidates):
    lowest = 82
    seasons = ['2023-24','2022-23','2021-22','2020-21','2019-20','2018-19','2017-18','2016-17','2015-16','2014-15','2013-14',
          '2012-13','2011-12','2010-11','2009-10','2008-09','2007-08','2006-07', 
    ]

    df = pd.read_csv('MIPs.csv')
    df['MIP Rank'] = df['MIP Rank'].str.replace('T', '').astype(int)

    

    with open('min_games_by_top_'+ str(top_n_candidates) +'_candidates_report.txt', 'w') as file:
        
        for season in seasons:
            # Filter the DataFrame based on the condition
            filtered_players = df[(df['MIP Rank'] <= top_n_candidates) & (df['Season'] == season)]
            # Extract the list of player names
            candidate_names = filtered_players['Player'].tolist()
            
            # Get previous season
            prev_season = get_previous_season(season)
            prev_season_df = pd.read_csv(prev_season + '-PerGame.csv')
            
            for candidate in candidate_names:
                games_played = prev_season_df.loc[prev_season_df['Player'].str.contains(candidate, case=False, na=False), 'G'].values
                try:
                    games = games_played[0]

                except:
                    file.write(f"{candidate} played no games last year\n")
                
                else:
                    lowest = min(games, lowest)
                    file.write(f"{candidate} has played {games} in {prev_season}\n\n")
        
        # Write the final results
        file.write("Found all games played in the previous year\n")
        file.write(f"Minimum games played is {lowest}\n")

def find_lowest_games_same_season(top_n_candidates):
    lowest = 82
    seasons = ['2023-24','2022-23','2021-22','2020-21','2019-20','2018-19','2017-18','2016-17','2015-16','2014-15','2013-14',
          '2012-13','2011-12','2010-11','2009-10','2008-09','2007-08','2006-07'
    ]

    df = pd.read_csv('MIPs.csv')
    df['MIP Rank'] = df['MIP Rank'].str.replace('T', '').astype(int)

    

    with open('lowest_games_by_top_'+ str(top_n_candidates) +'_same_season_report.txt', 'w') as file:
        
        for season in seasons:
            # Filter the DataFrame based on the condition
            filtered_players = df[(df['MIP Rank'] <= top_n_candidates) & (df['Season'] == season)]
            # Extract the list of player names
            candidate_names = filtered_players['Player'].tolist()
            
           
            season_df = pd.read_csv(season + '-PerGame.csv')
            
            for candidate in candidate_names:
                games_played = season_df.loc[season_df['Player'].str.contains(candidate, case=False, na=False), 'G'].values
                try:
                    games = games_played[0]

                except:
                    file.write(f"{candidate} played no games this year\n")
                
                else:
                    lowest = min(games, lowest)
                    file.write(f"{candidate} has played {games} in {season}\n\n")
        
        # Write the final results
        file.write("Found all games played in the same year\n")
        file.write(f"Minimum games played is {lowest}\n")


def find_highest_PER(top_n_candidates):
    highest = 0
    highest_player = None
    highest_season = None
    seasons = ['2023-24','2022-23','2021-22','2020-21','2019-20','2018-19','2017-18','2016-17','2015-16','2014-15','2013-14',
          '2012-13','2011-12','2010-11','2009-10','2008-09','2007-08','2006-07' #'2005-06', '2004-05', '2003-04',
    ]

    df = pd.read_csv('MIPs.csv')
    df['MIP Rank'] = df['MIP Rank'].str.replace('T', '').astype(int)

    with open('highest_per_by_top_'+ str(top_n_candidates) +'_candidates_report.txt', 'w') as file:
        
        for season in seasons:
            # Filter the DataFrame based on the condition
            filtered_players = df[(df['MIP Rank'] <= top_n_candidates) & (df['Season'] == season)]
            # Extract the list of player names
            candidate_names = filtered_players['Player'].tolist()
            
            season_df = pd.read_csv(season + ' Advanced.csv')
            
            for candidate in candidate_names:
                per_values = season_df.loc[season_df['Player'].str.contains(candidate, case=False, na=False), 'PER'].values
                try:
                    per = per_values[0]

                except:
                    file.write(f"{candidate} has no recorded PER\n")
                
                else:
                    if per > highest:
                        highest_player = candidate
                        highest_season = season
                    highest = max(per, highest)
                   
                    file.write(f"{candidate} has PER of {per} in {season}\n\n")
        
        # Write the final results
        file.write("Since 2006-07 season,\n")
        file.write(f"Highest PER is {highest}, by {highest_player} in {highest_season}\n")

def add_won_already_column():
    # Read your CSV file
    csv_file = 'MIPs.csv'
    df = pd.read_csv(csv_file)

    # Step 2: Add the new column with value 'N' for all rows
    df['Won already'] = 'N'

    # Step 3: Save the updated DataFrame back to a CSV if needed
    df.to_csv('MIPs.csv', index=False)
    print("Already Won column updated successfully!")


def add_prev_games_column():
    seasons = ['2023-24','2022-23','2021-22','2020-21','2019-20','2018-19','2017-18','2016-17','2015-16','2014-15','2013-14',
        '2012-13','2011-12','2010-11','2009-10','2008-09','2007-08','2006-07', 
    ]

    for season in seasons:
        current_season_df = pd.read_csv(season + '-PerGame.csv')
        
        prev_season = get_previous_season(season)
        prev_season_df = pd.read_csv(prev_season + '-PerGame.csv')
       
        # Keep only the 'Player' and 'G' columns from the previous season and rename 'G' to 'G_prev'
        prev_season_df = prev_season_df[['Player', 'G']].rename(columns={'G': 'G_prev'})


        # Drop duplicate players, keeping the first occurrence from the previous season
        prev_season_first = prev_season_df.drop_duplicates(subset='Player', keep='first')
        # Create a dictionary to map players to their 'G_prev' value
        player_g_map = dict(zip(prev_season_first['Player'], prev_season_first['G_prev']))
        # Use the mapping to add the 'G_prev' column to current_season_df
        current_season_df['G_prev'] = current_season_df['Player'].map(player_g_map)
        # Fill any NaN values in 'G_prev' with 0
        current_season_df['G_prev'] = current_season_df['G_prev'].fillna(0)

        current_season_df.to_csv(season + '-PerGame.csv', index=False)

def add_total_prev_games_column():
    # List of seasons from the earliest to the latest
    seasons = ['2001-02', '2002-03', '2003-04', '2004-05', '2005-06', '2006-07', '2007-08', '2008-09', '2009-10',
               '2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16', '2016-17', '2017-18', '2018-19',
               '2019-20', '2020-21', '2021-22', '2022-23', '2023-24']
    
    # Only player with an extra season of games unaccounted for that was an mip winner
    players_games = {'Hedo Türkoğlu': 74}

    # Iterate through seasons in chronological order
    for season in seasons:
        # Read the current season's data
        current_season_df = pd.read_csv(season + '-PerGame.csv')

        # Add a column for total games played before the current season
        current_season_df['G_prev_total'] = current_season_df['Player'].apply(lambda player: players_games.get(player, 0))

        # Track the players we’ve processed in the current season
        processed_players = set()

        # Iterate over players in the current season
        for index, row in current_season_df.iterrows():
            player = row['Player']
            games_played = row['G']

            # Only add games for the first occurrence of the player
            if player not in processed_players:
                # Update the player's total games in the dictionary
                if player in players_games:
                    players_games[player] += games_played
                else:
                    players_games[player] = games_played
                processed_players.add(player)

        # Write the updated DataFrame to a new CSV file (or overwrite if that's desired)
        current_season_df.to_csv(season + '-PerGame-Updated.csv', index=False)


# Function to add a column of # seasons played to the current year in Seasons Played column
def add_seasons_prev():
    # List of seasons from the earliest to the latest
    seasons = ['2001-02', '2002-03', '2003-04', '2004-05', '2005-06', '2006-07', '2007-08', '2008-09', '2009-10',
               '2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16', '2016-17', '2017-18', '2018-19',
               '2019-20', '2020-21', '2021-22', '2022-23', '2023-24']
    
    # Only player with an extra season of games unaccounted for that was an mip winner
    players_seasons = {'Hedo Türkoğlu': 1}

    # Iterate through seasons in chronological order
    for season in seasons:
        # Read the current season's data
        current_season_df = pd.read_csv('Updated Per Game Seasons/'+season + '-PerGame-Updated.csv')

        # Add a column for total games played before the current season
        current_season_df['Seasons Played'] = current_season_df['Player'].apply(lambda player: players_seasons.get(player, 0))

        # Track the players we’ve processed in the current season
        processed_players = set()

        # Iterate over players in the current season
        for index, row in current_season_df.iterrows():
            player = row['Player']
            played_season = row['G'] > 35 # Min number games to be considered a season played in this case is 35

            # Only add games for the first occurrence of the player
            if player not in processed_players:
                # Update the player's total games in the dictionary
                if player in players_seasons:
                    if played_season:
                        players_seasons[player] += 1
                else:
                    if played_season:
                        players_seasons[player] = 1
                    else:
                        players_seasons[player] = 0
                processed_players.add(player)

        # Write the updated DataFrame to a new CSV file (or overwrite if that's desired)
        current_season_df.to_csv(season + '-PerGame-Updated.csv', index=False)


# Function to add a column of # seasons played to the current year in Seasons Played column

def add_prev_season_stats():
    # List of seasons from the earliest to the latest
    seasons = ['2006-07', '2007-08', '2008-09', '2009-10',
               '2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16', '2016-17', '2017-18', '2018-19',
               '2019-20', '2020-21', '2021-22', '2022-23', '2023-24']
    
    # Only player with an extra season of games unaccounted for that was an mip winner
    players_seasons = {}

    # Iterate through seasons in chronological order
    for season in seasons:
        # Read the current season's data
        current_season_df = pd.read_csv('Updated Per Game Seasons/'+season + '-PerGame-Updated.csv')
        
        prev_season = get_previous_season(season)
        prev_season_df = pd.read_csv('Updated Per Game Seasons/'+prev_season + '-PerGame-Updated.csv')
        games_played_prev_season = 0
        while games_played_prev_season < 35:
            pass

        # Add a column for total games played before the current season
        current_season_df['Seasons Played'] = current_season_df['Player'].apply(lambda player: players_seasons.get(player, 0))

        # Track the players we’ve processed in the current season
        processed_players = set()

        # Iterate over players in the current season
        for index, row in current_season_df.iterrows():
            player = row['Player']
            played_season = row['G'] > 35 # Min number games to be considered a season played in this case is 35

            # Only add games for the first occurrence of the player
            if player not in processed_players:
                # Update the player's total games in the dictionary
                if player in players_seasons:
                    if played_season:
                        players_seasons[player] += 1
                else:
                    if played_season:
                        players_seasons[player] = 1
                    else:
                        players_seasons[player] = 0
                processed_players.add(player)

        # Write the updated DataFrame to a new CSV file (or overwrite if that's desired)
        current_season_df.to_csv(season + '-PerGame-Updated.csv', index=False)

####START
####
# Helper function to get the previous season string
def get_previous_season2(current_season, seasons):
    current_idx = seasons.index(current_season)
    if current_idx > 0:
        return seasons[current_idx - 1]
    return None  # If no previous season exists

# Helper function to find a valid previous season where the player played >= 35 games
def find_valid_prev_season(player, current_season, seasons, min_games=35):
    previous_season = get_previous_season2(current_season, seasons)
    while previous_season:
        try:
            prev_season_df = pd.read_csv(f'Updated Per Game Seasons/{previous_season}-PerGame-Updated.csv')
            prev_player_row = prev_season_df[prev_season_df['Player'] == player]
            
            # Check if the player played at least min_games in the previous season
            if not prev_player_row.empty and prev_player_row['G'].values[0] >= min_games:
                return prev_player_row  # Return the row if valid
        except FileNotFoundError:
            pass  # Ignore missing files and move to the next season

        # Move to the season before this one
        previous_season = get_previous_season2(previous_season, seasons)
    
    return None  # If no valid previous season is found

# Main function to add the previous season stats columns
def add_previous_season_columns():
    # List of seasons from the earliest to the latest
    seasons = ['2006-07', '2007-08', '2008-09', '2009-10',
               '2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16', '2016-17', '2017-18', '2018-19',
               '2019-20', '2020-21', '2021-22', '2022-23', '2023-24']

    # Stats columns to track from the previous season
    stat_columns = ['G', 'GS', 'MP', 'FG', 'FGA', '3P', '3PA', '2P', '2PA', 'FT', 'FTA', 
                    'DRB', 'TRB', 'AST', 'BLK', 'TOV', 'PTS']

    # Reverse the seasons list to process from the earliest to the latest
    seasons.reverse()

    # Iterate through seasons in chronological order
    for season in seasons:
        # Read the current season's data
        current_season_df = pd.read_csv(f'Updated Per Game Seasons/{season}-PerGame-Updated.csv')

        # Initialize 'X_prev_season' columns for current season
        for stat in stat_columns:
            current_season_df[f'{stat}_prev_season'] = 0

        # Track the players we’ve processed in the current season
        processed_players = set()

        # Iterate over players in the current season
        for index, row in current_season_df.iterrows():
            player = row['Player']

            # If the player has played at least one season
            if row['Seasons Played'] > 0:
                # Find a valid previous season for this player
                prev_player_row = find_valid_prev_season(player, season, seasons)
                
                if prev_player_row is not None:
                    # Copy stats from the valid previous season to the current season
                    for stat in stat_columns:
                        current_season_df.at[index, f'{stat}_prev_season'] = prev_player_row[stat].values[0]

            # Only update the stats for the first occurrence of a player in the season
            if player not in processed_players:
                processed_players.add(player)

        # Write the updated DataFrame to a new CSV file (or overwrite if desired)
        current_season_df.to_csv(f'Updated Per Game Seasons/{season}-PerGame-Updated.csv', index=False)

def add_previous_season_col():
     # List of seasons from the earliest to the latest
    seasons = ['2001-02',# '2002-03', '2003-04', '2004-05',
      #  '2005-06','2006-07', '2007-08', '2008-09', '2009-10',
       #       '2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16', '2016-17', '2017-18', '2018-19',
        #       '2019-20', '2020-21', '2021-22', '2022-23', '2023-24'
       ]
    
    for season in seasons:
        # Read the current season's data
        current_season_df = pd.read_csv(f'Updated Per Game Seasons/{season}-PerGame-Updated.csv')
        current_season_advanced_df = pd.read_csv(f'Updated Per Game Seasons/{season}-Advanced-Updated.csv')

        # For each player, find their previous valid season (over 35 games played)
        for index, row in current_season_df.iterrows():
            player = row['Player']
            # If the player hasn't previously played at least one season, set None
            if row['Seasons Played'] == 0:
                current_season_df.at[index, 'Previous Season'] = "None"
                current_season_advanced_df.loc[current_season_advanced_df['Player'] == player, 'Previous Season'] = "None"
            else:
                previous_season = get_previous_season(season)
                previous_season_df = pd.read_csv(f'Updated Per Game Seasons/{previous_season}-PerGame-Updated.csv')
                #previous_season_advanced_df = pd.read_csv(f'{previous_season} Advanced.csv')
                try:
                    g_prev = previous_season_df.loc[previous_season_df['Player'] == player, 'G'].values[0]
                except:
                    print(player + " did not play in " + previous_season)
                    g_prev = 0
                # Wait to find the previous valid season
                while not g_prev or g_prev < 35:
                    previous_season = get_previous_season(previous_season)
                    previous_season_df = pd.read_csv(f'Updated Per Game Seasons/{previous_season}-PerGame-Updated.csv')
                    #previous_season_advanced_df = pd.read_csv(f'{previous_season} Advanced.csv')
                    try:
                        g_prev = previous_season_df.loc[previous_season_df['Player'] == player, 'G'].values[0]
                        
                    except:
                        print(player + " did not play in " + previous_season)

                # Once we've found the right season, add it to Pergame and Advanced data
                current_season_df.at[index, 'Previous Season'] = previous_season
                current_season_advanced_df.loc[current_season_advanced_df['Player'] == player, 'Previous Season'] = previous_season
                
        current_season_df.to_csv(f'Updated Per Game Seasons/{season}-PerGame-Updated.csv', index=False)
        current_season_advanced_df.to_csv(f'Updated Per Game Seasons/{season}-Advanced-Updated.csv', index=False)


def add_best_season_col():
     # List of seasons from the earliest to the latest
    seasons = ['2006-07', '2007-08', '2008-09', '2009-10',
              '2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16', '2016-17', '2017-18', '2018-19',
               '2019-20', '2020-21', '2021-22', '2022-23', '2023-24'
       ]
    
    for season in seasons:
        # Read the current season's data
        current_season_df = pd.read_csv(f'Updated Per Game Seasons/{season}-PerGame-Updated.csv')
        current_season_advanced_df = pd.read_csv(f'Updated Per Game Seasons/{season}-Advanced-Updated.csv')

        # For each player, find their previous valid season (over 35 games played)
        for index, row in current_season_df.iterrows():
            player = row['Player']
            best_season = "None"
            prev_seasons_checked = 0
            best_ppg = 0

            # If the player hasn't previously played at least one season, set None
            if row['Seasons Played'] == 0:
                current_season_df.at[index, 'Best Season'] = "None"
                current_season_advanced_df.loc[current_season_advanced_df['Player'] == player, 'Best Season'] = "None"
            else:
                previous_season = get_previous_season(season)
                previous_season_df = pd.read_csv(f'Updated Per Game Seasons/{previous_season}-PerGame-Updated.csv')
                prev_seasons_checked += 1
                
                try:
                    g_prev = previous_season_df.loc[previous_season_df['Player'] == player, 'G'].values[0]
                    if g_prev >= 35:
                        ppg = previous_season_df.loc[previous_season_df['Player'] == player, 'PTS'].values[0]
                        if ppg > best_ppg:
                            best_ppg = ppg
                            best_season = previous_season
                except:
                    #print(player + " did not play in " + previous_season)
                    g_prev = 0

                # Wait to find the previous valid season from past 8 seasons
                while prev_seasons_checked <= 8 and previous_season != "2001-02":
                    previous_season = get_previous_season(previous_season)
                    previous_season_df = pd.read_csv(f'Updated Per Game Seasons/{previous_season}-PerGame-Updated.csv')
                    prev_seasons_checked += 1
                    
                    try:
                        g_prev = previous_season_df.loc[previous_season_df['Player'] == player, 'G'].values[0]
                        if g_prev >= 35:
                            ppg = previous_season_df.loc[previous_season_df['Player'] == player, 'PTS'].values[0]
                        if ppg > best_ppg:
                            best_ppg = ppg
                            best_season = previous_season
                    except:
                       #print(player + " did not play in " + previous_season)
                        g_prev = 0

                # Once we've found the right season, add it to Pergame and Advanced data
                current_season_df.at[index, 'Best Season'] = best_season
                current_season_advanced_df.loc[current_season_advanced_df['Player'] == player, 'Best Season'] = best_season
                
        current_season_df.to_csv(f'Updated Per Game Seasons/{season}-PerGame-Updated.csv', index=False)
        current_season_advanced_df.to_csv(f'Updated Per Game Seasons/{season}-Advanced-Updated.csv', index=False)

def add_previous_season_values():
     # List of seasons from the earliest to the latest
    seasons = ['2006-07', '2007-08', '2008-09', '2009-10',
               '2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16', '2016-17', '2017-18', '2018-19',
               '2019-20', '2020-21', '2021-22', '2022-23', '2023-24']
    
    for season in seasons:
        # Read the current season's data
        current_season_df = pd.read_csv(f'Updated Per Game Seasons/{season}-PerGame-Updated.csv')
        current_season_advanced_df = pd.read_csv(f'Updated Per Game Seasons/{season}-Advanced-Updated.csv')

        # For each player, find their previous valid season (over 35 games played)
        for index, row in current_season_df.iterrows():
            previous_season = row['Previous Season']
            player = row['Player']
            
            #print("Player is " + player)
    

            # If their last season was in 2001 we most likely don't care about them
            if not pd.isna(previous_season) and previous_season != "2001-02":
                previous_season_df = pd.read_csv(f'Updated Per Game Seasons/{previous_season}-PerGame-Updated.csv')
                first_occurrence = previous_season_df.loc[previous_season_df['Player'] == player].head(1)

                #print("SEASON: " + season)
                #print("prev year is " + previous_season + ", PLAYER is " + player)

                previous_season_advanced_df = pd.read_csv(f'Updated Per Game Seasons/{previous_season}-Advanced-Updated.csv')
                first_occurrence_advanced = previous_season_advanced_df.loc[previous_season_advanced_df['Player'] == player].head(1)
                
                
                # Get previous season pergame values
                current_season_df.loc[current_season_df['Player'] == player, 'PS_PTS'] = first_occurrence['PTS'].values[0]
                current_season_df.loc[current_season_df['Player'] == player, 'PS_TRB'] = first_occurrence['TRB'].values[0]
                current_season_df.loc[current_season_df['Player'] == player, 'PS_AST'] = first_occurrence['AST'].values[0]
                current_season_df.loc[current_season_df['Player'] == player, 'PS_STL'] = first_occurrence['STL'].values[0]
                current_season_df.loc[current_season_df['Player'] == player, 'PS_BLK'] = first_occurrence['BLK'].values[0]
                current_season_df.loc[current_season_df['Player'] == player, 'PS_MP'] = first_occurrence['MP'].values[0]
                current_season_df.loc[current_season_df['Player'] == player, 'PS_G'] = first_occurrence['G'].values[0]
                current_season_df.loc[current_season_df['Player'] == player, 'PS_FGA'] = first_occurrence['FGA'].values[0]
                current_season_df.loc[current_season_df['Player'] == player, 'PS_FG'] = first_occurrence['FG'].values[0]
                current_season_df.loc[current_season_df['Player'] == player, 'PS_TOV'] = first_occurrence['TOV'].values[0]
                current_season_df.loc[current_season_df['Player'] == player, 'PS_PTS'] = first_occurrence['PTS'].values[0]
                current_season_df.loc[current_season_df['Player'] == player, 'PS_3P'] = first_occurrence['3P'].values[0]
                current_season_df.loc[current_season_df['Player'] == player, 'PS_3PA'] = first_occurrence['3PA'].values[0]
                current_season_df.loc[current_season_df['Player'] == player, 'PS_2P'] = first_occurrence['2P'].values[0]
                current_season_df.loc[current_season_df['Player'] == player, 'PS_3P%'] = first_occurrence['3P%'].values[0]
                current_season_df.loc[current_season_df['Player'] == player, 'PS_2PA'] = first_occurrence['2PA'].values[0]
                current_season_df.loc[current_season_df['Player'] == player, 'PS_2P%'] = first_occurrence['2P%'].values[0]
                current_season_df.loc[current_season_df['Player'] == player, 'PS_FT%'] = first_occurrence['FT%'].values[0]

                current_season_advanced_df.loc[current_season_advanced_df['Player'] == player, 'PS_PER'] = first_occurrence_advanced['PER'].values[0]
                current_season_advanced_df.loc[current_season_advanced_df['Player'] == player, 'PS_TRB%'] = first_occurrence_advanced['TRB%'].values[0]
                current_season_advanced_df.loc[current_season_advanced_df['Player'] == player, 'PS_AST%'] = first_occurrence_advanced['AST%'].values[0]
                current_season_advanced_df.loc[current_season_advanced_df['Player'] == player, 'PS_BPM'] = first_occurrence_advanced['BPM'].values[0]
                current_season_advanced_df.loc[current_season_advanced_df['Player'] == player, 'PS_VORP'] = first_occurrence_advanced['VORP'].values[0]
                current_season_advanced_df.loc[current_season_advanced_df['Player'] == player, 'PS_USG%'] = first_occurrence_advanced['USG%'].values[0]
                current_season_advanced_df.loc[current_season_advanced_df['Player'] == player, 'PS_WS'] = first_occurrence_advanced['WS'].values[0]
                current_season_advanced_df.loc[current_season_advanced_df['Player'] == player, 'PS_WS/48'] = first_occurrence_advanced['WS/48'].values[0]

            else:
                current_season_df.loc[current_season_df['Player'] == player, 'PS_PTS'] = 0
                current_season_df.loc[current_season_df['Player'] == player, 'PS_TRB'] = 0
                current_season_df.loc[current_season_df['Player'] == player, 'PS_AST'] = 0
                current_season_df.loc[current_season_df['Player'] == player, 'PS_STL'] = 0
                current_season_df.loc[current_season_df['Player'] == player, 'PS_BLK'] = 0
                current_season_df.loc[current_season_df['Player'] == player, 'PS_MP'] = 0
                current_season_df.loc[current_season_df['Player'] == player, 'PS_G'] = 0
                current_season_df.loc[current_season_df['Player'] == player, 'PS_FGA'] = 0
                current_season_df.loc[current_season_df['Player'] == player, 'PS_FG'] = 0
                current_season_df.loc[current_season_df['Player'] == player, 'PS_TOV'] = 0
                current_season_df.loc[current_season_df['Player'] == player, 'PS_PTS'] = 0
                current_season_df.loc[current_season_df['Player'] == player, 'PS_3P'] = 0
                current_season_df.loc[current_season_df['Player'] == player, 'PS_3PA'] = 0
                current_season_df.loc[current_season_df['Player'] == player, 'PS_2P'] = 0
                current_season_df.loc[current_season_df['Player'] == player, 'PS_3P%'] = 0
                current_season_df.loc[current_season_df['Player'] == player, 'PS_2PA'] = 0
                current_season_df.loc[current_season_df['Player'] == player, 'PS_2P%'] = 0
                current_season_df.loc[current_season_df['Player'] == player, 'PS_FT%'] =0

                current_season_advanced_df.loc[current_season_advanced_df['Player'] == player, 'PS_PER'] = 0
                current_season_advanced_df.loc[current_season_advanced_df['Player'] == player, 'PS_TRB%'] = 0
                current_season_advanced_df.loc[current_season_advanced_df['Player'] == player, 'PS_AST%'] = 0
                current_season_advanced_df.loc[current_season_advanced_df['Player'] == player, 'PS_BPM'] = 0
                current_season_advanced_df.loc[current_season_advanced_df['Player'] == player, 'PS_VORP'] = 0
                current_season_advanced_df.loc[current_season_advanced_df['Player'] == player, 'PS_USG%'] = 0
                current_season_advanced_df.loc[current_season_advanced_df['Player'] == player, 'PS_WS'] = 0
                current_season_advanced_df.loc[current_season_advanced_df['Player'] == player, 'PS_WS/48'] = 0

        current_season_df.to_csv(f'Updated Per Game Seasons/{season}-PerGame-Updated.csv', index=False)
        current_season_advanced_df.to_csv(f'Updated Per Game Seasons/{season}-Advanced-Updated.csv', index=False) 


def add_best_season_values():
     # List of seasons from the earliest to the latest
    seasons = ['2006-07', '2007-08', '2008-09', '2009-10',
               '2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16', '2016-17', '2017-18', '2018-19',
               '2019-20', '2020-21', '2021-22', '2022-23', '2023-24']
    
    for season in seasons:
        # Read the current season's data
        current_season_df = pd.read_csv(f'Updated Per Game Seasons/{season}-PerGame-Updated.csv')
        current_season_advanced_df = pd.read_csv(f'Updated Per Game Seasons/{season}-Advanced-Updated.csv')

        # For each player, find their previous valid season (over 35 games played)
        for index, row in current_season_df.iterrows():
            best_season = row['Best Season']
            player = row['Player']
            
            #print("Player is " + player)
    

            # If their last season was in 2001 we most likely don't care about them
            if not pd.isna(best_season) and best_season != "2001-02":
                previous_season_df = pd.read_csv(f'Updated Per Game Seasons/{best_season}-PerGame-Updated.csv')
                first_occurrence = previous_season_df.loc[previous_season_df['Player'] == player].head(1)

                #print("SEASON: " + season)
                #print("prev year is " + previous_season + ", PLAYER is " + player)

                previous_season_advanced_df = pd.read_csv(f'Updated Per Game Seasons/{best_season}-Advanced-Updated.csv')
                first_occurrence_advanced = previous_season_advanced_df.loc[previous_season_advanced_df['Player'] == player].head(1)
                
                
                # Get previous season pergame values
                current_season_df.loc[current_season_df['Player'] == player, 'BS_PTS'] = first_occurrence['PTS'].values[0]
                current_season_df.loc[current_season_df['Player'] == player, 'BS_TRB'] = first_occurrence['TRB'].values[0]
                current_season_df.loc[current_season_df['Player'] == player, 'BS_AST'] = first_occurrence['AST'].values[0]
                current_season_df.loc[current_season_df['Player'] == player, 'BS_STL'] = first_occurrence['STL'].values[0]
                current_season_df.loc[current_season_df['Player'] == player, 'BS_BLK'] = first_occurrence['BLK'].values[0]
                current_season_df.loc[current_season_df['Player'] == player, 'BS_MP'] = first_occurrence['MP'].values[0]
                current_season_df.loc[current_season_df['Player'] == player, 'BS_G'] = first_occurrence['G'].values[0]
                current_season_df.loc[current_season_df['Player'] == player, 'BS_FGA'] = first_occurrence['FGA'].values[0]
                current_season_df.loc[current_season_df['Player'] == player, 'BS_FG'] = first_occurrence['FG'].values[0]
                current_season_df.loc[current_season_df['Player'] == player, 'BS_TOV'] = first_occurrence['TOV'].values[0]
                current_season_df.loc[current_season_df['Player'] == player, 'BS_PTS'] = first_occurrence['PTS'].values[0]
                current_season_df.loc[current_season_df['Player'] == player, 'BS_3P'] = first_occurrence['3P'].values[0]
                current_season_df.loc[current_season_df['Player'] == player, 'BS_3PA'] = first_occurrence['3PA'].values[0]
                current_season_df.loc[current_season_df['Player'] == player, 'BS_2P'] = first_occurrence['2P'].values[0]
                current_season_df.loc[current_season_df['Player'] == player, 'BS_3P%'] = first_occurrence['3P%'].values[0]
                current_season_df.loc[current_season_df['Player'] == player, 'BS_2PA'] = first_occurrence['2PA'].values[0]
                current_season_df.loc[current_season_df['Player'] == player, 'BS_2P%'] = first_occurrence['2P%'].values[0]
                current_season_df.loc[current_season_df['Player'] == player, 'BS_FT%'] = first_occurrence['FT%'].values[0]

                current_season_advanced_df.loc[current_season_advanced_df['Player'] == player, 'BS_PER'] = first_occurrence_advanced['PER'].values[0]
                current_season_advanced_df.loc[current_season_advanced_df['Player'] == player, 'BS_TRB%'] = first_occurrence_advanced['TRB%'].values[0]
                current_season_advanced_df.loc[current_season_advanced_df['Player'] == player, 'BS_AST%'] = first_occurrence_advanced['AST%'].values[0]
                current_season_advanced_df.loc[current_season_advanced_df['Player'] == player, 'BS_BPM'] = first_occurrence_advanced['BPM'].values[0]
                current_season_advanced_df.loc[current_season_advanced_df['Player'] == player, 'BS_VORP'] = first_occurrence_advanced['VORP'].values[0]
                current_season_advanced_df.loc[current_season_advanced_df['Player'] == player, 'BS_USG%'] = first_occurrence_advanced['USG%'].values[0]
                current_season_advanced_df.loc[current_season_advanced_df['Player'] == player, 'BS_WS'] = first_occurrence_advanced['WS'].values[0]
                current_season_advanced_df.loc[current_season_advanced_df['Player'] == player, 'BS_WS/48'] = first_occurrence_advanced['WS/48'].values[0]

            else:
                current_season_df.loc[current_season_df['Player'] == player, 'BS_PTS'] = 0
                current_season_df.loc[current_season_df['Player'] == player, 'BS_TRB'] = 0
                current_season_df.loc[current_season_df['Player'] == player, 'BS_AST'] = 0
                current_season_df.loc[current_season_df['Player'] == player, 'BS_STL'] = 0
                current_season_df.loc[current_season_df['Player'] == player, 'BS_BLK'] = 0
                current_season_df.loc[current_season_df['Player'] == player, 'BS_MP'] = 0
                current_season_df.loc[current_season_df['Player'] == player, 'BS_G'] = 0
                current_season_df.loc[current_season_df['Player'] == player, 'BS_FGA'] = 0
                current_season_df.loc[current_season_df['Player'] == player, 'BS_FG'] = 0
                current_season_df.loc[current_season_df['Player'] == player, 'BS_TOV'] = 0
                current_season_df.loc[current_season_df['Player'] == player, 'BS_PTS'] = 0
                current_season_df.loc[current_season_df['Player'] == player, 'BS_3P'] = 0
                current_season_df.loc[current_season_df['Player'] == player, 'BS_3PA'] = 0
                current_season_df.loc[current_season_df['Player'] == player, 'BS_2P'] = 0
                current_season_df.loc[current_season_df['Player'] == player, 'BS_3P%'] = 0
                current_season_df.loc[current_season_df['Player'] == player, 'BS_2PA'] = 0
                current_season_df.loc[current_season_df['Player'] == player, 'BS_2P%'] = 0
                current_season_df.loc[current_season_df['Player'] == player, 'BS_FT%'] =0

                current_season_advanced_df.loc[current_season_advanced_df['Player'] == player, 'BS_PER'] = 0
                current_season_advanced_df.loc[current_season_advanced_df['Player'] == player, 'BS_TRB%'] = 0
                current_season_advanced_df.loc[current_season_advanced_df['Player'] == player, 'BS_AST%'] = 0
                current_season_advanced_df.loc[current_season_advanced_df['Player'] == player, 'BS_BPM'] = 0
                current_season_advanced_df.loc[current_season_advanced_df['Player'] == player, 'BS_VORP'] = 0
                current_season_advanced_df.loc[current_season_advanced_df['Player'] == player, 'BS_USG%'] = 0
                current_season_advanced_df.loc[current_season_advanced_df['Player'] == player, 'BS_WS'] = 0
                current_season_advanced_df.loc[current_season_advanced_df['Player'] == player, 'BS_WS/48'] = 0

        current_season_df.to_csv(f'Updated Per Game Seasons/{season}-PerGame-Updated.csv', index=False)
        current_season_advanced_df.to_csv(f'Updated Per Game Seasons/{season}-Advanced-Updated.csv', index=False) 
# ONE TIME USE
# 
#
def remove_extra_letters_from_name():
    seasons = [ '2005-06', '2004-05', '2003-04', '2002-03', '2001-02'
    ]

    for season in seasons:
        current_season_df = pd.read_csv(season + '-PerGame.csv')
        current_season_df['Player'] = current_season_df['Player'].str.replace(r'[\*\\].*', '', regex=True)
        current_season_df.to_csv(season + '-PerGame.csv', index=False)

        advanced_df = pd.read_csv(season + ' Advanced.csv')
        advanced_df['Player'] = advanced_df['Player'].str.replace(r'[\*\\].*', '', regex=True)
        advanced_df.to_csv(season + ' Advanced.csv', index=False)

        total_df = pd.read_csv(season + ' Total.csv')
        total_df['Player'] = total_df['Player'].str.replace(r'[\*\\].*', '', regex=True)
        total_df.to_csv(season + ' Total.csv', index=False)

def add_previous_seed_col():
     # List of seasons from the earliest to the latest
    seasons = ['2006-07', '2007-08', '2008-09', '2009-10',
               '2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16', '2016-17', '2017-18', '2018-19',
               '2019-20', '2020-21', '2021-22', '2022-23', '2023-24']
    
    for season in seasons:
        # Read the current season's data
        current_standings = pd.read_csv(season + ' Standings.csv')
        previous_standings = pd.read_csv(get_previous_season(season) + ' Standings.csv')

        for index, row in current_standings.iterrows():
            team = row['Team']
            if team == 'New Orleans Hornets' and season == '2007-08':
                team = 'New Orleans/Oklahoma City Hornets'
            elif team == 'Oklahoma City Thunder' and season == '2008-09':
                team = 'Seattle SuperSonics'
            elif team == 'Brooklyn Nets' and season == '2012-13':
                team = 'New Jersey Nets'
            elif team == 'New Orleans Pelicans' and season == '2013-14':
                team = 'New Orleans Hornets'
            elif team == 'Charlotte Hornets' and season == '2014-15':
                team = 'Charlotte Bobcats'
            current_standings.loc[current_standings['Team'] == team, 'Previous Seed'] =  previous_standings.loc[previous_standings['Team'] == team]["Seed"].values[0]
            
            #print(team + " in " + season+ " PREV SEED = " + str(previous_standings.loc[previous_standings['Team'] == team]["Seed"].values[0]))
        current_standings.to_csv(f'Updated Per Game Seasons/{season}-Standings-Updated.csv', index=False) 

def add_difference_seed_col():
     # List of seasons from the earliest to the latest
    seasons = ['2006-07', '2007-08', '2008-09', '2009-10',
               '2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16', '2016-17', '2017-18', '2018-19',
               '2019-20', '2020-21', '2021-22', '2022-23', '2023-24']

    for season in seasons:
        # Read the current season's data
        current_standings = pd.read_csv(f'Updated Per Game Seasons/{season}-Standings-Updated.csv')

        for index, row in current_standings.iterrows():
            curr_seed = row['Seed']
            prev_seed = row['Previous Seed']
            current_standings.loc[index, 'Seed Difference'] = prev_seed - curr_seed # backwards bc if they go down in seed the team got better
            
            #print(team + " in " + season+ " PREV SEED = " + str(previous_standings.loc[previous_standings['Team'] == team]["Seed"].values[0]))
        current_standings.to_csv(f'Updated Per Game Seasons/{season}-Standings-Updated.csv', index=False) 


def add_season_col():
    season = '2024-25'

    mvps = pd.read_csv(f'/Users/von/Desktop/Work/Projects/NBA_MIP_Predictor/WNBA-MVP/Data/MVPs.csv')
    for i, row in mvps.iterrows():
        if row['Rank'] == '1':
            season = get_previous_season(season)
        mvps.loc[i, 'Season'] = season

    mvps.to_csv(f'/Users/von/Desktop/Work/Projects/NBA_MIP_Predictor/WNBA-MVP/Data/MVPs.csv', index=False)

def test_drop_dupes():

    pergame= pd.read_csv(f'/Users/von/Desktop/Work/Projects/NBA_MIP_Predictor/WNBA-MVP/Data/Pergame-Stats/2023-24-Pergame.csv')
    # Sort by Player and set 'TOT' as priority for Team
    pergame = pergame.sort_values(by=['Player', 'Team'], key=lambda x: x == 'TOT', ascending=False)

    # Drop duplicates based on Player, keeping the first occurrence ('TOT' prioritized)
    pergame = pergame.drop_duplicates(subset='Player', keep='first')

    pergame.to_csv(f'/Users/von/Desktop/Work/Projects/NBA_MIP_Predictor/WNBA-MVP/Data/test.csv', index=False)


# Confirmed no MVP candidate was traded that same year
def check_mvp_candidate_traded():
    season = '2023-24'
    season_df =  pd.read_csv(f'/Users/von/Desktop/Work/Projects/NBA_MIP_Predictor/WNBA-MVP/Data/Pergame-Stats/2023-24-Pergame.csv')

    mvps = pd.read_csv(f'/Users/von/Desktop/Work/Projects/NBA_MIP_Predictor/WNBA-MVP/Data/MVPs.csv')
    for i, row in mvps.iterrows():
        player_name = row['Player']

        if season != row['Season']:
            season = row['Season']
            season_df = pd.read_csv(f'/Users/von/Desktop/Work/Projects/NBA_MIP_Predictor/WNBA-MVP/Data/Pergame-Stats/{season}-Pergame.csv')
        player_rows = season_df.loc[(season_df['Player'] == player_name)&(season_df['Team'] == 'TOT')]
        if len(player_rows) > 0:
            print("MVP CANDIDATE " + player_name + " was on two teams.")



def rename_MPG_col():
    seasons = ['2003-04','2004-05','2005-06','2006-07', '2007-08', '2008-09', '2009-10',
               '2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16', '2016-17', '2017-18', '2018-19',
               '2019-20', '2020-21', '2021-22', '2022-23', '2023-24']
    #seasons = ['2003-04']
    for season in seasons:
        df = pd.read_csv(f'/Users/von/Desktop/Work/Projects/NBA_MIP_Predictor/WNBA-MVP/Data/Total-Stats/{season}-Totals.csv')

        print("Original columns:", df.columns)

        # Remove the second 'MP' column
        # Here we keep the first 'MP' by slicing the DataFrame
        df = df.drop(df.columns[[5,7]], axis=1)

        df.rename(columns={'MP.1': 'MPG'}, inplace=True)
        df.to_csv(f'/Users/von/Desktop/Work/Projects/NBA_MIP_Predictor/WNBA-MVP/Data/Total-Stats/{season}-Totals.csv', index=False)

def find_lowest_x(top_n_candidates, col_name):
    lowest = 100000
    lowest_player = None
    lowest_season = None
    rank_num = 1
    seasons = ['2023-24','2022-23','2021-22','2020-21','2019-20','2018-19','2017-18','2016-17','2015-16','2014-15','2013-14',
          '2012-13','2011-12','2010-11','2009-10','2008-09','2007-08','2006-07','2005-06', '2004-05', '2003-04',
    ]

    df = pd.read_csv(f'/Users/von/Desktop/Work/Projects/NBA_MIP_Predictor/WNBA-MVP/Data/MVPs.csv')
    df['MVP Rank'] = df['MVP Rank'].str.replace('T', '').astype(int)

    with open(f'lowest_{col_name}_by_top_'+ str(top_n_candidates) +'_candidates_report.txt', 'w') as file:
        
        for season in seasons:
            # Filter the DataFrame based on the condition
            filtered_players = df[(df['MVP Rank'] <= top_n_candidates) & (df['Season'] == season)]
            # Extract the list of player names
            candidate_names = filtered_players['Player'].tolist()
            
            season_df = pd.read_csv(f'/Users/von/Desktop/Work/Projects/NBA_MIP_Predictor/WNBA-MVP/Data/Advanced-Stats/{season}-Advanced.csv')
            
            for candidate in candidate_names:
                per_values = season_df.loc[season_df['Player'].str.contains(candidate, case=False, na=False), col_name].values
               
                try:
                    val = per_values[0]

                except:
                    file.write(f"{candidate} has no recorded {col_name}\n")
                
                else:
                    if val < lowest:
                        lowest_player = candidate
                        lowest_season = season
                    lowest = min(val, lowest)
                   
                    file.write(f"{candidate} has {col_name} of {val} in {season}, rank is {rank_num}\n\n")
        
        # Write the final results
        file.write("Since 2003-04 season,\n")
        file.write(f"Lowest {col_name} is {lowest}, by {lowest_player} in {lowest_season}\n")


if __name__ == "__main__":
    

    #add_won_already_column()
    #add_previous_season_values()
    #add_best_season_col()
   # check_mvp_candidate_traded()
    #rename_MPG_col()
    find_lowest_x(3, "PER")
    #test_drop_dupes()
    #add_best_season_values()
    #add_previous_season_col()
    # Update the "Season" column by filling missing or invalid values
    #df = fill_missing_seasons(df, 'Season')

    #find_lowest_games_season_before(3)
    #find_lowest_games_same_season(5)
    #find_highest_PER(5)
    
    #add_seasons_prev()
    #add_total_prev_games_column()
    #remove_extra_letters_from_name()



    #print("Lowest games prev", lowest_games_prev)
   



'''
if __name__ == "__main__":
    # Read your CSV file
    csv_file = 'MIPs_updated.csv'
    df = pd.read_csv(csv_file)

    lowest_pts_differential = 99.0
    lowest_reb_differential = 99.0
    lowest_ast_differential = 99.0

    for i, row in df.iterrows():
        lowest_pts_differential = min(lowest_pts_differential, row["PTS_Differential"])
        lowest_reb_differential = min(lowest_reb_differential, row["REB_Differential"])
        lowest_ast_differential = min(lowest_ast_differential, row["AST_Differential"])


    print("Lowest pts diff - ", lowest_pts_differential)
    print("Lowest reb diff - ", lowest_reb_differential)
    print("Lowest ast diff - ", lowest_ast_differential)

'''