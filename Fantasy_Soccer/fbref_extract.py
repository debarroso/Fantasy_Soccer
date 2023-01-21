##########################################################################################
# File: fbref_extract.py
# File Created: Tuesday, 23rd March 2021 6:48:13 pm
# Author: Oliver DeBarros
# -----
# Last Modified: Sunday, 6th February 2022 4:58:58 pm
# Modified By: Oliver DeBarros
# -----
# Description:
#   This file stores all of the methods related to extracting data from fbref.com
##########################################################################################


import datetime as dt
import fbref_lib as fb
import time


"""
Performs a historical load for the specified league (default is all) from
fbref.com as far back as their first season specified in the config file
"""
def full_match_historical_extract(league=None):

    #get leagues dict and iterate over keys
    leagues = fb.get_league_dict(league)
    
    for league in leagues:
        
        #get the season links from the history page
        seasons = fb.get_seasons(leagues[league]['link'])
        
        for season_url in seasons:

            #for some reason the history page returns stats so convert to the fixtures url
            fixture_url = fb.stats_url_to_fixtures_url(season_url)
            fixture_url_split = fixture_url.split("/")

            #if there are only 6 sections, hasnt been indexed by fbref so this is the current season
            if len(fixture_url_split) == 6:
                year = leagues[league]['current_season']

            else:
                year = int(fixture_url_split[-1].split("-")[0])

            if year < leagues[league]['first_season']:
                continue

            #gets all of the match report links from the fixtures page
            matches = fb.get_match_reports(fb.get_homepage() + fixture_url)

            #save each match request to a file
            for match in matches:
                time.sleep(5)
                fb.save_match_file(match, year, league)


"""
Performs a daily extract for dates within passed in lookback period from yesterday.
Will overwrite existing files with new requests
Parameters:
    lookback_days - number of days to lookback from yesterday (default is 7)
"""
def daily_match_extract(lookback_days=7):

    #grab league dict object and notable dates
    league_dict = fb.get_league_dict()
    yesterday = dt.date.today() - dt.timedelta(days=1)
    begin_date = yesterday - dt.timedelta(days=lookback_days)

    #increment begin_date by 1 in this loop until it equals yesterday
    while begin_date <= yesterday:

        time.sleep(3)

        #get matches dict {League: [matches]}
        matches = fb.get_matchday_matches(f"{fb.get_homepage()}/en/matches/{begin_date}")

        #save each match file
        for league in matches:
            for match in matches[league]:
                time.sleep(3)
                fb.save_match_file(match, league_dict[league]['current_season'], league)

        begin_date = begin_date + dt.timedelta(days=1)


"""
Pulls match extracts for a passed in range of dates (only supports a single season)
Parameters:
    dates - list of dates to iterate over and perform extracts
    season - determines which season to save the data
"""
def ad_hoc_match_extract(dates, season):
    
    #iterate over dates
    for date in dates:

        time.sleep(3)
        
        #get matches dict {League: [matches]}
        matches = fb.get_matchday_matches(f"{fb.get_homepage()}/en/matches/{date}")

        #save each match file
        for league in matches:
            for match in matches[league]:
                time.sleep(3)
                fb.save_match_file(match, season, league)

daily_match_extract()