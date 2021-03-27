##########################################################################################
# File: fbref_lib.py
# File Created: Tuesday, 23rd March 2021 6:33:29 pm
# Author: Oliver DeBarros (debarros.oliver@gmail.com)
# -----
# Last Modified: Saturday, 27th March 2021 5:23:39 pm
# Modified By: Oliver DeBarros (debarros.oliver@gmail.com)
# -----
#  This script stores methods for returning links from passed in links
##########################################################################################


import requests, os, json, re
import datetime as dt
import pandas as pd
from bs4 import BeautifulSoup


"""
Returns string of homepage for the football reference site
"""
def get_homepage():

    return "https://fbref.com"


"""
Returns the directory of this file
"""
def get_directory():

    return "{}\\".format(os.path.dirname(__file__))


"""
Method for building the file structure making up the "data lake" and config
fbref_links file if they do not exist
"""
def build_directories():

    build_sample_config()

    leagues = get_league_dict()
    
    if not os.path.exists(get_directory() + "Seasons"):
        os.makedirs(get_directory() + "Seasons")

    for league in leagues:

        #set to earliest year in this db history
        year = 2017

        while year <= leagues[league]["current_season"]:

            if not os.path.exists(get_directory() + "Seasons\\{}".format(year)):
                os.makedirs(get_directory() + "Seasons\\{}".format(year))

            if not os.path.exists(get_directory() + "Seasons\\{}\\FBref_Match_HTMLs".format(year)):
                os.makedirs(get_directory() + "Seasons\\{}\\FBref_Match_HTMLs".format(year))

            if not os.path.exists(get_directory() + "Seasons\\{}\\FBref_Match_HTMLs\\{}".format(year, league)):
                os.makedirs(get_directory() + "Seasons\\{}\\FBref_Match_HTMLs\\{}".format(year, league))

            year += 1

"""
Builds an example config file
"""
def build_sample_config():
    if not os.path.exists(get_directory() + "fbref_links.json"):
        sample_dict = {
            "***Substitute with League Name Key***": {
                "id": "***Go to https://fbref.com/en/comps/ and see what number comes next when you hover over hyperlinks***",
                "current_season": "***Beginning year of the most current season (for now updated manually)***",
                "link": "***The competition link to the season history if you were to click on it at https://fbref.com/en/comps/***"
            }
        }

        with open(get_directory() + "fbref_links.json", "w") as fp:
            fp.write(json.dumps(sample_dict, indent=4))



"""
Returns a league dict object with data for request parameters
Parameters:
    league - if looking for a specific league pass it in
"""
def get_league_dict(league=None):

    with open(get_directory() + "fbref_links.json") as fp:
        league_dict = json.load(fp)

    if league:
        return league_dict[league]
    
    else:
        return league_dict


"""
Since season history pulls stats pages, this method converts to the fixtures url
Parameters:
    season_stats_url - url of the stats page for this league
"""
def stats_url_to_fixtures(season_stats_url):
    
    split_url = season_stats_url.split("/")
    
    return "{}/schedule/{}".format("/".join(split_url[:-1]), split_url[-1].replace("Stats", "Scores-and-Fixtures"))



"""
Returns the soup object for a passed in source
Parameters:
    source - input text to get soup for, can be url or html as text
"""
def get_soup(source):
    
    #in case this is a url, try a request first
    try:
        page_html = requests.get(source).text
    except:
        #if the request failed I assume html was passed in as text
        page_html = source
    
    return BeautifulSoup(page_html, features="lxml")


"""
Returns a list containing links to all seasons for a league
Parameters:
    link - url link to the league fbref page
"""
def get_seasons(link):

    #get a soup object for the seasons section of the league page
    soup = get_soup(link)
    seasons = get_soup(str(soup.find(id="div_seasons")))
    
    links = seasons.find_all("a")
    
    #remove duplicates and get list of comps links
    season_links = [str(link).split("\"")[1] for link in links if "comps" in str(link)]
    season_links = list(set(season_links))

    return season_links


"""
Returns a list containing links to all matches in a season
Parameters:
    link - url link to any fbref page
"""
def get_match_reports(link):
    
    #get all link html tags
    soup = get_soup(link)
    matches = soup.find_all("a")
    
    #check that this is a Match Report link and add to a list, dedupe at end
    match_links = [str(link).split("\"")[1] for link in matches if "matches" in str(link) and "Match Report" in str(link)]
    match_links = list(set(match_links))

    return match_links


"""
Save a match report in the directory
Parameters:
    link - url suffix of match report (does not include homepage)
    year - the year corresponding to the bucket in the directory
    league - the league competition this match was played in
"""
def save_match_file(link, year, league):
    
    #get html request and store file name
    page_text = requests.get(get_homepage() + link).text
    file_name = link.replace("/", "_")[1:] + ".txt"

    #write request to file
    fp = open("{}Seasons\\{}\\FBref_Match_HTMLs\\{}\\{}".format(get_directory(), year, league, file_name), "w", encoding="utf-8")
    fp.write(page_text)
    fp.close()    


"""
Returns the links to the matches played in selected competitions
(stored in fbref_links.json) for the given match date
Parameters:
    link - url link to the match date web page
"""
def get_matchday_matches(link):

    #get league dict object for active leagues
    league_dict = get_league_dict()
    
    #get soup object and table tags
    soup = get_soup(link)
    tables = soup.find_all("table")
    
    #initialize list to store match links
    matches = {}

    for table in tables:

        #the table caption should tell us which league this is
        caption = table.find("caption").find("a")

        #find the league in the dict and save matches to file
        for league in league_dict:

            #this league is in the league_dict
            if "/en/comps/{}/".format(league_dict[league]["id"]) in str(caption):
                matches[league] = get_match_reports(str(table))

    return matches


"""
Parses a stat table from a fbref match report and returns
a list of dicts to create a dataframe from
Parameters:
    table - html text within <table> tags
"""
def parse_stat_table(table):

    #get all rows from tbody html tags
    table_rows = []
    rows = table.find("tbody").find_all("tr")

    for row in rows:

        #if this is a spacer row, there is no data so skip
        try:
            if "spacer" in row.get("class"):
                continue
        except:
            pass

        row_dict = {}
        columns = row.find_all(["th", "td"])

        #iterate over columns and output to rows
        for column in columns:
            try:
                link = column.find("a").get("href")

                #save if this is a player link
                if "players" in link:
                    row_dict["{}_link".format(column.get("data-stat"))] = link

                #save player country link
                elif "country" in link:
                    row_dict["country_link"] = link
                    row_dict["nationality"] = link.split('/')[-2]
                    continue

            except:
                print("Error parsing column {} in stats table...".format(column))
            
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

    #get lineup html tags
    lineups = soup.find_all("div", {"class": "lineup"})
    lineup_list = []
    home = True
    
    for lineup in lineups:
        
        rows = lineup.find_all("tr")
        
        #get team info and indicate these are starters until flipped
        team = rows[0].get_text().split("(")[0].strip()
        formation = rows[0].get_text().split("(")[1].strip(")")
        starter = True

        for row in rows[1:]:
            
            #flip switch to show we are now looking at the bench
            if "Bench" in row.get_text():
                starter = False
                continue

            #write object to return list
            lineup_list.append(
                {
                    "team": team,
                    "home": home,
                    "formation": formation,
                    "starter": starter,
                    "player_link": str(row).split("\"")[1]
                }
            )
        
        #second time through this loop is for the away team
        home = False

    return lineup_list


"""
Returns match meta data from match file
Parameters:
    text - html page request as text
"""
def get_match_metadata(text):
    
    #get soup and initialize return dict
    soup = get_soup(text)
    metadata = {}

    #grab header metadata from webpage
    metadata["matchweek"] = soup.find("div", {"class": "box"}).div.get_text()
    metadata["competition_link"] = soup.find("div", {"class": "box"}).div.find("a").get("href")
    scorebox = soup.find("div", {"class": "scorebox"})
    teams = {
        "home": scorebox.div,
        "away": scorebox.div.find_next_sibling("div")
    }

    #get team specific metadata
    for team in teams:
        
        metadata["{}_team".format(team)] = teams[team].find("a").get_text()
        metadata["{}_record".format(team)] = teams[team].find_all("div")[5].get_text()
        metadata["{}_score".format(team)] = int(teams[team].find("div", {"class": "score"}).get_text())
        metadata["{}_manager".format(team)] = teams[team].find("div", {"class": "datapoint"}).get_text().replace("Manager: ", "").replace(u"\xa0", u" ")
        
        #not every match has this statistic, if it doesn't just set to none type
        try:
            metadata["{}_xg".format(team)] = float(teams[team].find("div", {"class": "score_xg"}).get_text())
        except:
            metadata["{}_xg".format(team)] = None

        #if the record string doesn't match this pattern it wasn't there
        pattern = re.compile("([0-9])+-([0-9])+-([0-9])+")
        if not pattern.search(metadata["{}_record".format(team)]):
            metadata["{}_record".format(team)] = None
        
    #get scorebox metadata if it exists
    scorebox_meta = soup.find("div", {"class": "scorebox_meta"}).find_all("small")
    for element in scorebox_meta:
        
        if "Attendance" in element:
            metadata["attendance"] = get_soup(str(scorebox_meta[scorebox_meta.index(element)+1])).get_text()

        if "Venue" in element:
            metadata["venue"] = get_soup(str(scorebox_meta[scorebox_meta.index(element)+1])).get_text()

        if "Officials" in element:
            metadata["officials"] = get_soup(str(scorebox_meta[scorebox_meta.index(element)+1])).get_text().replace(u"\xa0", u" ").replace(" · ", ",")

    return metadata


"""
Parses match report html file and returns dict of dataframes
Parameters:
    file_path - windows file path of match report file
"""
def parse_lake_file(file_path):

    #open file in the lake and remove html comments
    fp = open(file_path, "r", encoding="utf-8")
    text = fp.read().replace('<!--', '').replace('-->', '')
    fp.close()
    
    table_dict = {}

    #get team and game data for this match
    lineups = get_team_lineups(text)
    match_meta = get_match_metadata(text)

    #add dataframes to return object
    table_dict["Lineups"] = pd.DataFrame(lineups)
    table_dict["Match_Metadata"] = pd.DataFrame(columns=match_meta.keys()).append(match_meta, ignore_index=True)

    #iterate over all table objects
    for table in get_soup(text).find_all("table"):

        #only stats tables should work
        try:

            title = table.find("caption").get_text()
            data = parse_stat_table(table)
            df = pd.DataFrame(data)

            if title not in table_dict:
                table_dict[title] = []
        
            table_dict[title].append(df)

        except:
            print("Error {} is not a stats table and could not be parsed...".format(table))
            continue
    
    #if there is no shots table ignore the exception
    try:
        table_dict["Shots Table"] = table_dict["Shots Table"][0]
    except:
        print("Error parsing shots table...")
    
    return table_dict