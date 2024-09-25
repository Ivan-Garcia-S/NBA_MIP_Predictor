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


if __name__ == "__main__":
    # Read your CSV file
    csv_file = 'MIPs.csv'
    df = pd.read_csv(csv_file)

    # Step 2: Add the new column with value 'N' for all rows
    df['Won already'] = 'N'

    # Step 3: Save the updated DataFrame back to a CSV if needed
    df.to_csv('MIPs.csv', index=False)
    # Update the "Season" column by filling missing or invalid values
    #df = fill_missing_seasons(df, 'Season')

    # Find differential of stats from previous year.
    #df, lowest_games_prev = find_differential_of_stats(df)
    #df.to_csv('MIPs_updated.csv', index=False)



    #print("Lowest games prev", lowest_games_prev)
    print("Already Won column updated successfully!")



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