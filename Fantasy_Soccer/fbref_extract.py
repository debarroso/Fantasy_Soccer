##########################################################################################
# File: fbref_extract.py
# File Created: Tuesday, 23rd March 2021 6:48:13 pm
# Author: Oliver DeBarros (debarros.oliver@gmail.com)
# -----
# Last Modified: Wednesday, 24th March 2021 11:19:00 pm
# Modified By: Oliver DeBarros (debarros.oliver@gmail.com)
# -----
# Description:
#   This file stores all of the methods related to extracting data from fbref.com
##########################################################################################


import fbref_lib as fb


"""
Performs a historical load for the selected leagues from fbref.com
as far back as 2017 as that is when the site updated their statistics tables
"""
def full_historical_extract():

    #get leagues dict and iterate over keys
    leagues = fb.get_league_dict()
    
    for league in leagues:
        
        #get the season links from the history page
        seasons = fb.get_seasons(leagues[league]["link"])
        
        for season_url in seasons:

            #for some reason the history page returns stats so convert to the fixtures url
            fixture_url = fb.stats_url_to_fixtures(season_url)
            fixture_url_split = fixture_url.split("/")

            #if there are only 6 sections, hasnt been indexed by fbref so this is the current season
            if len(fixture_url_split) == 6:
                year = leagues[league]["current_season"]

            else:
                year = int(fixture_url_split[-1].split("-")[0])

            if year < 2017:
                continue

            #gets all of the match report links from the fixtures page
            matches = fb.get_match_reports(fb.get_homepage() + fixture_url)

            #save each match request to a file
            for match in matches:
                fb.save_match_file(match, year, league)


def daily_extract():
    pass

def ad_hoc_extract():
    pass