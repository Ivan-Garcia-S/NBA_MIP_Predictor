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

if __name__ == "__main__":
    

    #add_won_already_column()


    # Update the "Season" column by filling missing or invalid values
    #df = fill_missing_seasons(df, 'Season')

    #find_lowest_games_season_before(3)
    #find_lowest_games_same_season(5)
    #find_highest_PER(5)
    
    add_seasons_prev()
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