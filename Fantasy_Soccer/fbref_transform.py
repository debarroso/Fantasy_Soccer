##########################################################################################
# File: fbref_transform.py
# File Created: Tuesday, 23rd March 2021 6:37:32 pm
# Author: Oliver DeBarros (debarros.oliver@gmail.com)
# -----
# Last Modified: Tuesday, 23rd March 2021 6:38:32 pm
# Modified By: Oliver DeBarros (debarros.oliver@gmail.com)
# -----
# Description:
#   Transforms fbref match report data into the various tables to push to the DB
##########################################################################################


import fbref_lib as fb
import pandas as pd
import glob


def main():

    file_list = get_files([2017, 2018, 2019, 2020])
    
    for lake_file in file_list:
        tables = fb.parse_lake_file(lake_file)

        for table in tables:
            table_df = table


"""
Returns a list of files for whichever seasons are passed in
Parameters:
    seasons - list of seasons to grab files from
"""
def get_files(seasons):

    file_list = []

    for year in seasons:
        for thing in glob.glob('{}Seasons\\{}\\FBref_Match_HTMLs\\*\\*'.format(fb.get_directory(), year)):
            file_list.append(thing)

    return file_list
    

"""
Returns a joined dataframe from a list of dataframes and removes duplicate columns
Parameters:
    df_list - list of dataframes
"""
def combine_dataframes(df_list): 
    
    df = pd.concat(df_list, axis=1, sort=False)
    df = df.loc[:,~df.columns.duplicated()]

    return df


if __name__ == "__main__":
    main()