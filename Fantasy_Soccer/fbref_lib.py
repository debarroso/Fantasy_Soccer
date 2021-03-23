##########################################################################################
# File: fbref_lib.py
# File Created: Tuesday, 23rd March 2021 6:33:29 pm
# Author: Oliver DeBarros (debarros.oliver@gmail.com)
# -----
# Last Modified: Tuesday, 23rd March 2021 6:33:57 pm
# Modified By: Oliver DeBarros (debarros.oliver@gmail.com)
# -----
#  This script stores methods for returning links from passed in links
##########################################################################################


import requests, os, json
import datetime as dt
import pandas as pd
from bs4 import BeautifulSoup


"""
Returns string of homepage for the football reference website
"""
def get_homepage():
    return "https://fbref.com/en/"


"""
Returns the directory of this file
"""
def get_directory():
    return "{}\\".format(os.path.dirname(__file__))


"""
Returns the links for the passed in competition
Parameters:
    league - if looking for a specific league pass it in
"""
def get_competition_links(league=None):

    with open(get_directory() + "fbref_links.json") as fp:
        league_dict = json.load(fp)

    if league:
        return league_dict[league]
    
    else:
        return league_dict

"""
Returns the soup object for a passed in source
    try to process a request in case the source is a url
Parameters:
    source - input text to get soup for, can be url or html as text
"""
def get_soup(source):
    
    try:
        page_html = requests.get(source).text
    except:
        page_html = source
    
    return BeautifulSoup(page_html, features="lxml")


"""
Returns a list containing links to all seasons for a league
Parameters:
    link - url link to the league web page
"""
def get_seasons(link):

    soup = get_soup(link)
    seasons = get_soup(str(soup.find(id="div_seasons")))
    
    links = seasons.find_all("a")
    
    season_links = [str(link).split("\"")[1] for link in links if "comps" in str(link)]
    season_links = list(set(season_links))

    return season_links


"""
Returns a list containing links to all matches in a season
Parameters:
    link - url link to the leason season webpage
"""
def get_matches(link):
    
    soup = get_soup(link)
    matches = get_soup(str(soup.find(id="all_kitchen_sink_sched")))
    
    links = matches.find_all("a")
    
    match_links = [str(link).split("\"")[1] for link in links if "matches" in str(link) and "Match Report" in str(link)]
    match_links = list(set(match_links))

    return match_links


"""
Returns the links to the matches played for the given match date
Parameters:
    link - url link to the match date web page
"""
def get_matchday_matches(link):
    
    soup = get_soup(link)
    matches = soup.find_all("table")
    leagues = get_competition_links()
    league_matches = {}

    for match in matches:
        soup = get_soup(str(match))
        league_link = str(soup.find("caption").find("a"))

        for key in leagues:
            if "comps/{}/".format(leagues[key]["id"]) in league_link:
                
                links = soup.find_all("a")
                match_links = [str(link).split("\"")[1] for link in links if "matches" in str(link) and "Match Report" in str(link)]
                match_links = list(set(match_links))
                
                league_matches[key] = match_links

    return league_matches


"""
Parses a stat table from a fbref match report
Parameters:
    table - html text within <table> tags
"""
def parse_stat_table(table):

    table_rows = []
    rows = table.find("tbody").find_all("tr")

    for row in rows:

        try:
            if "spacer" in row.get("class"):
                continue
        except:
            pass

        row_dict = {}
        columns = row.find_all(["th", "td"])

        for column in columns:
            try:
                link = column.find("a").get("href")

                if "players" in link:
                    row_dict["{}_link".format(column.get("data-stat"))] = link

                elif "country" in link:
                    row_dict["country_link"] = link
                    row_dict["nationality"] = link.split('/')[-2]
                    continue

            except:
                pass
            
            row_dict[column.get("data-stat")] = column.get_text(strip=True)

        table_rows.append(row_dict)

    return table_rows


"""
Parses the team data from a fbref match report
Parameters:
    text - html request page as text
"""
def get_team_lineups(text):

    soup = get_soup(text)
    lineups = soup.find_all("div", {"class": "lineup"})
    lineup_list = []
    home = True
    
    for lineup in lineups:
        
        rows = lineup.find_all("tr")
        
        team = rows[0].get_text().split("(")[0].strip()
        formation = rows[0].get_text().split("(")[1].strip(")")
        starter = True

        for row in rows[1:]:
            
            if "Bench" in row.get_text():
                starter = False
                continue

            lineup_list.append(
                {
                    "team": team,
                    "home": home,
                    "formation": formation,
                    "starter": starter,
                    "player_link": str(row).split("\"")[1]
                }
            )
        
        home = False

    return lineup_list


"""
Returns match meta data from match file
Parameters:
    text - html page request as text
"""
def get_match_metadata(text):
    
    soup = get_soup(text)
    metadata = {}
    metadata["matchweek"] = soup.find("div", {"class": "box"}).div.get_text()
    scorebox = soup.find("div", {"class": "scorebox"})
    teams = {
        "home": scorebox.div,
        "away": scorebox.div.find_next_sibling("div")
    }

    for team in teams:
        metadata["{}_team".format(team)] = teams[team].find("a").get_text()
        metadata["{}_record".format(team)] = teams[team].find_all("div")[5].get_text()
        metadata["{}_score".format(team)] = int(teams[team].find("div", {"class": "score"}).get_text())
        metadata["{}_xg".format(team)] = float(teams[team].find("div", {"class": "score_xg"}).get_text())
        metadata["{}_manager".format(team)] = teams[team].find("div", {"class": "datapoint"}).get_text().replace("Manager: ", "").replace(u"\xa0", u" ")

    scorebox_meta = soup.find("div", {"class": "scorebox_meta"}).find_all("small")
    metadata["venue"] = get_soup(str(scorebox_meta[1])).get_text()
    metadata["officials"] = get_soup(str(scorebox_meta[-1])).get_text().replace(u"\xa0", u" ").replace(" · ", ",")

    return metadata


"""
Parses match report html file and returns dict of dataframes
Parameters:
    file_path - windows file path of match report file
"""
def parse_lake_file(file_path):

    fp = open(file_path, "r", encoding="utf-8")
    text = fp.read().replace('<!--', '').replace('-->', '')
    fp.close()
    
    table_dict = {}

    lineups = get_team_lineups(text)
    match_meta = get_match_metadata(text)

    table_dict["Lineups"] = pd.DataFrame(lineups)
    table_dict["Match_Metadata"] = pd.DataFrame(columns=match_meta.keys()).append(match_meta, ignore_index=True)

    for table in get_soup(text).find_all("table"):
        try:

            title = table.find("caption").get_text()
            data = parse_stat_table(table)
            df = pd.DataFrame(data)

            if title not in table_dict:
                table_dict[title] = []
        
            table_dict[title].append(df)

        except:
            continue

    table_dict["Shots Table"] = table_dict["Shots Table"][0]
    
    return table_dict