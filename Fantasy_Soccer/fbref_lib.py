##########################################################################################
# File: fbref_lib.py
# File Created: Tuesday, 23rd March 2021 6:33:29 pm
# Author: Oliver DeBarros
# -----
# Last Modified: Sunday, 6th February 2022 4:58:13 pm
# Modified By: Oliver DeBarros
# -----
# Description:
#   This script stores methods for returning links from passed in links
##########################################################################################


import requests, os, json, re, glob, random, calendar
import datetime as dt
import pandas as pd
from bs4 import BeautifulSoup


"""
Returns string of homepage for the football reference site
"""
def get_homepage():
    return "https://fbref.com"


"""
Returns the directory of this file as a string
"""
def get_directory():
    return f"{os.path.dirname(__file__)}\\"


"""
Returns the directory of this user
"""
def get_user_directory():
    return f"{os.path.expanduser('~')}\\"


"""
Method for building the file structure making up the "data lake" and config
fbref_links file if they do not exist
"""
def build_directories():

    build_sample_config()

    leagues = get_league_dict()
    
    if not os.path.exists(get_directory() + "Seasons"):
        os.makedirs(get_directory() + "Seasons")

    if not os.path.exists(get_directory() + "DB"):
        os.makedirs(get_directory() + "DB")

    if not os.path.exists(get_directory() + "Testing"):
        os.makedirs(get_directory() + "Testing")

    for league in leagues:

        #set to earliest year in this db history
        year = leagues[league]['first_season']

        while year <= leagues[league]['current_season']:

            if not os.path.exists(get_directory() + f"Seasons\\{year}"):
                os.makedirs(get_directory() + f"Seasons\\{year}")

            if not os.path.exists(get_directory() + f"Seasons\\{year}\\FBref_Match_HTMLs"):
                os.makedirs(get_directory() + f"Seasons\\{year}\\FBref_Match_HTMLs")

            if not os.path.exists(get_directory() + f"Seasons\\{year}\\FBref_Match_HTMLs\\{league}"):
                os.makedirs(get_directory() + f"Seasons\\{year}\\FBref_Match_HTMLs\\{league}")

            if leagues[league]['rotowire'] is True:
                if not os.path.exists(get_directory() + f"Seasons\\{year}\\Rotowire"):
                    os.makedirs(get_directory() + f"Seasons\\{year}\\Rotowire")

                if not os.path.exists(get_directory() + f"Seasons\\{year}\\Rotowire\\{league}"):
                    os.makedirs(get_directory() + f"Seasons\\{year}\\Rotowire\\{league}")

                if not os.path.exists(get_directory() + f"Seasons\\{year}\\Rotowire\\{league}\\Players"):
                    os.makedirs(get_directory() + f"Seasons\\{year}\\Rotowire\\{league}\\Players")

                if not os.path.exists(get_directory() + f"Seasons\\{year}\\Rotowire\\{league}\\Teams"):
                    os.makedirs(get_directory() + f"Seasons\\{year}\\Rotowire\\{league}\\Teams")

            year += 1

"""
Builds an example config file
"""
def build_sample_config():
    if not os.path.exists(get_directory() + "fbref_links.json"):
        sample_dict = {
            "***Substitute with League Name Key***": {
                "id": "***Go to https://fbref.com/en/comps/ and see what number comes next when you hover over hyperlinks***",
                "first_season": "***First season to collect data from***",
                "current_season": "***Beginning year of the most current season (for now updated manually)***",
                "link": "***The competition link to the season history if you were to click on it at https://fbref.com/en/comps/***",
                "rotowire": "***Boolean to control whether or not I have rotowire data***"
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
        return {league: league_dict[league]}
    
    else:
        return league_dict


"""
Since season history pulls stats pages, this method converts to the fixtures url
Parameters:
    season_stats_url - url of the stats page for this league
"""
def stats_url_to_fixtures_url(season_stats_url):
    
    split_url = season_stats_url.split("/")
    
    return f"{'/'.join(split_url[:-1])}/schedule/{split_url[-1].replace('Stats', 'Scores-and-Fixtures')}"



"""
Returns the soup object for a passed in source
Parameters:
    source - input text to get soup for, can be url or html as text
"""
def get_soup(source):
    
    #in case this is a url, try a request first
    try:
        page_html = requests.get(source).text
    except Exception:
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
    with open(f"{get_directory()}Seasons\\{year}\\FBref_Match_HTMLs\\{league}\\{file_name}", "w", encoding="utf-8") as fp:
        fp.write(page_text)


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
            if f"/en/comps/{league_dict[league]['id']}/" in str(caption):
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
        except Exception:
            pass

        row_dict = {}
        columns = row.find_all(['th', 'td'])

        #iterate over columns and output to rows
        for column in columns:
            try:
                link = column.find("a").get("href")

                #save if this is a player link
                if "players" in link:
                    row_dict[f"{column.get('data-stat')}_link"] = link

                #save player country link
                elif "country" in link:
                    row_dict['country_link'] = link
                    row_dict['nationality'] = link.split('/')[-2]
                    continue

            except Exception:
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
    metadata['matchweek'] = soup.find("div", {"class": "box"}).div.get_text()
    
    # (deprecated) metadata['competition_link'] = soup.find("div", {"class": "box"}).div.find("a").get("href")
    
    scorebox = soup.find("div", {"class": "scorebox"})
    teams = {
        "home": scorebox.div,
        "away": scorebox.div.find_next_sibling("div")
    }

    #get team specific metadata
    for team in teams:
        
        metadata[f"{team}_team"] = teams[team].find("a").get_text()
        metadata[f"{team}_team_link"] = teams[team].find("a").get("href")
        metadata[f"{team}_record"] = teams[team].find_all("div")[5].get_text()
        metadata[f"{team}_score"] = int(teams[team].find("div", {"class": "score"}).get_text())
        metadata[f"{team}_manager"] = teams[team].find("div", {"class": "datapoint"}).get_text().replace("Manager: ", "").replace(u"\xa0", u" ")
        
        #not every match has this statistic, if it doesn't just set to none type
        try:
            metadata[f"{team}_xg"] = float(teams[team].find("div", {"class": "score_xg"}).get_text())
        except Exception:
            metadata[f"{team}_xg"] = None

        #if the record string doesn't match this pattern it wasn't there
        pattern = re.compile("([0-9])+-([0-9])+-([0-9])+")
        if not pattern.search(metadata[f"{team}_record"]):
            metadata[f"{team}_record"] = None
    
    #get the venue time of the match
    metadata['venuetime'] = soup.find("div", {"class": "scorebox_meta"}).find("span", {"class": "venuetime"}).get_text().replace(" (venue time)", "")

    #get scorebox metadata if it exists
    scorebox_meta = soup.find("div", {"class": "scorebox_meta"}).find_all("small")
    
    #set initial values
    metadata['attendance'] = None
    metadata['venue'] = None
    metadata['officials'] = None

    for element in scorebox_meta:
        
        if "Attendance" in element:
            metadata['attendance'] = int(get_soup(str(scorebox_meta[scorebox_meta.index(element)+1])).get_text().replace(",",""))

        if "Venue" in element:
            metadata['venue'] = get_soup(str(scorebox_meta[scorebox_meta.index(element)+1])).get_text()

        if "Officials" in element:
            metadata['officials'] = get_soup(str(scorebox_meta[scorebox_meta.index(element)+1])).get_text().replace(u"\xa0", u" ").replace(" · ", ",")

    return metadata


"""
Extracts the text formatted date from a match url and returns 'yyyy-mm-dd'
Parameters:
    file_path - file path of match report file
"""
def get_match_date(file_path):

    segments = file_path.split("-")
    date_segs = []

    for month in calendar.month_name:
        
        for segment in segments:

            if segment == month:
                index = segments.index(segment)
                date_segs = segments[index:index+3]

    match_datetime = dt.datetime.strptime(f"{date_segs[0]} {date_segs[1]} {date_segs[2]}", "%B %d %Y")
    match_date = str(match_datetime).split(" ")[0]

    return str(match_date)


"""
Returns the file name from the passed in string formatted path
Parameters:
    file_path - file path of match report file
"""
def get_file_name(file_path):
    return file_path.split("\\")[-1]


"""
Adds match id at the beginning of each row dict in a list
Parameters:
    in_dict - list of row dict objects for dataframes
    match_id - passed in match id
    match_date - passed in match date
    season - season folder this file came from
"""
def add_match_identifiers(in_dict, match_id, match_date, season):
    
    row = {}
    row['match_id'] = match_id
    row['match_date'] = match_date
    row['season'] = season
    row.update(in_dict)

    return row

"""
Parses match report html file and returns dict of dataframes
Parameters:
    file_path - file path of match report file
"""
def parse_lake_match_file(file_path, text):

    match_date = get_match_date(file_path)
    match_id = get_file_name(file_path).split("_")[2]
    season = file_path.split("\\")[-4]

    #open file in the lake and remove html comments
    # with open(file_path, "r", encoding="utf-8") as fp:
    #     text = fp.read().replace('<!--', '').replace('-->', '')
    
    table_dict = {}

    #iterate over rows in lineup and add match identifiers
    lineups = []
    for row in get_team_lineups(text):
        lineups.append(add_match_identifiers(row, match_id, match_date, season))
        
    #add match identifiers to parsed data
    match_meta = add_match_identifiers(get_match_metadata(text), match_id, match_date, season)

    #add dataframes to return object
    table_dict['Lineups'] = pd.DataFrame(lineups)
    table_dict['Match_Metadata'] = pd.DataFrame(columns=match_meta.keys()).append(match_meta, ignore_index=True)

    #iterate over all table objects
    for table in get_soup(text).find_all("table"):

        #only stats tables should work
        try:

            title = table.find("caption").get_text()

            #iterate over rows and add match indentifiers
            data = []
            for row in parse_stat_table(table):
                data.append(add_match_identifiers(row, match_id, match_date, season))

            df = pd.DataFrame(data)

            if title not in table_dict:
                table_dict[title] = []
        
            table_dict[title].append(df)

        except Exception:
            continue
    
    #if there is no shots table ignore the exception, also there are three
    #tables returned and we only care about the first (combined)
    try:
        table_dict['Shots Table'] = table_dict['Shots Table'][0]
    except Exception:
        pass
    
    return table_dict


"""
Returns a list of fbref.com files for whichever league season is passed in
If no values are passed it defaults to everything
Parameters:
    leagues - league to pull data from
    season - season to pull data from
"""
def get_fbref_files(leagues="*", season="*"):

    #if something other than a list was passed in, put it in a list
    if type(leagues) != list:
        leagues = [leagues]

    #initialize list of files for return
    file_list = []

    #iterate and return all files from each year
    for league in leagues:
        for thing in glob.glob(f"{get_directory()}Seasons\\{season}\\FBref_Match_HTMLs\\{league}\\*"):
            file_list.append(thing)

    return file_list


"""
Writes match tables from passed in dictionary to files
Parameters:
    tables - dictionary storing table dataframes
    mode - controls write mode of file
"""
def write_tables_to_files(tables, league, schema="raw", mode="w"):

    if league == "*":
        league = "All"

    if mode == "w":
        headers = True
    else:
        headers = False
    
    for table in tables:
        os.makedirs(f"{get_directory()}DB\\{league}\\{schema}", exist_ok=True)
        tables[table].to_csv(f"{get_directory()}DB\\{league}\\{schema}\\{table}.csv", index=False, mode=mode, columns=tables[table].columns, header=headers)
        

"""
Joins a list of dataframes and removes duplicative columns between them
Parameters:
    df_list - list of dataframes to join
"""
def full_lateral_df_join(df_list):

    #join dfs laterally then only keep one version of duplicate columns
    df = pd.concat(df_list, axis=1, sort=False)
    df = df.loc[:,~df.columns.duplicated()]

    return df


"""
Returns a randomized subset of a list for testing
Parameters:
    in_list - passed in list to pull from
    out_size - number of elements to return
    seed - seed to repeat random samples
"""
def shuffled_sample(in_list, out_size, seed=1):
    
    #down down do your dance x3
    random.Random(seed).shuffle(in_list)
    random.Random(seed).shuffle(in_list)
    random.Random(seed).shuffle(in_list)

    return in_list[:out_size]


"""
Converts the age string to number of days
Parameters:
    age_string - fbref formatted age YY-DDD
"""
def age_to_days(age_string):

    years = age_string.split("-")[0]
    days = age_string.split("-")[1]

    return (int(years) * 365) + int(days.lstrip("0"))


"""
Converts officials string into json object of crew
Parameters:
    officials - comma delimited string of officials
"""
def jsonify_officiating_crew(officials):

    officials_json = {}
    officials_list = officials.split(",")

    for official in officials_list:
        officials_json[official.split("(")[1].rstrip(")")] = official.split("(")[0].rstrip()

    return officials_json