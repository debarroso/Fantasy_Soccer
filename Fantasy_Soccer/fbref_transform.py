##########################################################################################
# File: fbref_transform.py
# File Created: Tuesday, 23rd March 2021 6:37:32 pm
# Author: Oliver DeBarros
# -----
# Last Modified: Thursday, 10th February 2022 8:47:48 pm
# Modified By: Oliver DeBarros
# -----
# Description:
#   Stores methods related to transforming data loaded from the data lake
##########################################################################################


import time, glob
import fbref_lib as fb
import pandas as pd
from concurrent import futures


"""
Iterates over files for a particular league in fbref and writes to a specified csv file
Parameters:
    league - league key to filter glob object
    season - season key to filter glob object
    write_mode - mode to write the csv as
"""
def fbref_tables(league="*", season="*", write_mode="w"):

    # get files for a particular league
    matches = fb.get_fbref_files(leagues=league, season=season)
    file_dict = {}

    # iterate over match files
    for match in matches:

        # read all files into memory to save on I/O operations
        with open(match, "r", encoding="utf-8") as fp:
            file_dict[match] = fp.read().replace('<!--', '').replace('-->', '')

    # intialize dict to store data frames
    df_dict = {
        'players': [],
        'goalkeepers': [],
        'lineups': [],
        'match_metadata': [],
        'shots_table': [],
    }

    # spin off new processes for performance
    with futures.ProcessPoolExecutor(max_workers=10) as executor:
        threads = [executor.submit(fb.parse_lake_match_file, match, file_dict[match]) for match in file_dict]

        # as processes complete process results
        for thread in futures.as_completed(threads):

            tables = thread.result()

            # append df to df_dict
            for table in tables:

                # if the first entry is a list do a lateral join on dfs
                if isinstance(tables[table], list):
                    df = fb.full_lateral_df_join(tables[table])

                if "Player" in str(table):
                    df_dict['players'].append(df)
                elif "Goalkeeper" in str(table):
                    df_dict['goalkeepers'].append(df)
                else:
                    key = str(table).lower().replace(" ", "_")
                    df_dict[key].append(tables[table])

    # depending on league some tables might be empty so check and flag them
    to_remove = []
    for key in df_dict:
        if len(df_dict[key]) == 0:
            to_remove.append(key)
        else:
            df_dict[key] = pd.concat(df_dict[key])

    # remove flagged tables
    [df_dict.pop(key) for key in to_remove]

    # write to file
    fb.write_tables_to_files(df_dict, league, mode=write_mode)


"""
Iterates over Rotowire files and writes to a specified csv file
Parameters:
    file_type - (Players or Teams) schemas are slightly different so specify the file type
    league - league key to filter glob object
    season - season key to filter glob object
    write_mode - mode to write the csv as
"""
def rotowire_tables(file_type="Players", league="*", season="*", write_mode="w"):

    # list to store all dfs in
    df_list = []

    # get all files and read into a df
    for f in glob.glob(f"{fb.get_directory()}\\Seasons\\{season}\\Rotowire\\{league}\\{file_type}\\*.csv"):
        
        df = pd.read_csv(f)
        df.insert(0, "week_file", f.split("\\")[-1].replace("week", "").replace(".csv", ""))
        df.insert(0, "league", f.split("\\")[-3])
        df.insert(0, "season", f.split("\\")[-5])
        df_list.append(df)

    # union all dataframes and reformat column headers
    combined = pd.concat(df_list)
    combined.columns = [column.lower().replace(" ", "_") for column in combined.columns]

    # write combined dataframes to file
    combined.to_csv(f"{fb.get_directory()}\\Testing\\rotowire_{league.lower()}_{file_type.lower()}.csv", index=False, mode=write_mode, columns=combined.columns, header=True)


if __name__ == "__main__":
    
    # keep track of processing time
    t1 = time.perf_counter()
    league = '*'
    fbref_tables(league=league, season="2022")
    print(f"Execution of {league} took: {(time.perf_counter() - t1)/60} min")

    # perform extract for each league
    # for league in fb.get_league_dict().keys():
        
        
        # rotowire_tables("Players", league)
        # rotowire_tables("Teams", league)
        
        # t1 = time.perf_counter()