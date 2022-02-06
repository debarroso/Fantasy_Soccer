##########################################################################################
# File: rotowire_scraper.py
# File Created: Wednesday, 1st September 2021 7:56:01 pm
# Author: Oliver DeBarros
# -----
# Last Modified: Sunday, 6th February 2021 4:20:03 pm
# Modified By: Oliver DeBarros
# -----
# Description:
#   Logs into my rotowire account and queries data sets based on settings
##########################################################################################


from selenium import webdriver
from selenium.webdriver.support.ui import Select
from cryptography.fernet import Fernet
import fbref_lib as fb
import time, os


league_dict = {
    "EPL": "Premier_League",
    "LIGA": "La_Liga",
    "SERI": "Serie_A",
    "FRAN": "Ligue_1",
    "BUND": "Bundesliga",
    "ENG_CH": "EFL_Championship",
    "UCL": "Champions_League",
    "UEL": "Europa_League",
    "MLS": "Major_League_Soccer"
}


with open(f"{fb.get_user_directory()}Documents\\key.key", "rb") as fp:
    key = fp.read()

f = Fernet(key)

creds = f.decrypt(os.getenv("rotowire").encode())
decoded = creds.decode().split("|")


"""
Logs into my rotowire account within web driver
"""
def login():
    driver.get("https://www.rotowire.com/users/login.php?go=%2F")
    driver.find_element_by_name("username").send_keys(decoded[0])
    driver.find_element_by_name("password").send_keys(decoded[1])
    driver.find_element_by_css_selector("button[class='btn primary full-width size-2 mb-20']").click()


"""
Makes initial selections to web pages before submitting query
---
Parameters:
    league - league to get data for
    player_extract - boolean to determine what type of extract to perform
"""
def download_csvs(league, player_extract):

    # depending on extract mode call approprate page and click on league links
    if player_extract:
        driver.get("https://www.rotowire.com/soccer/stats.php")
        driver.find_element_by_css_selector(f"div[data-name='{league}']").click()

    else:
        driver.get("https://www.rotowire.com/soccer/team-stats.php")
        driver.find_element_by_css_selector(f"a[data-val='{league}']").click()
    
    # select all elements
    driver.find_element_by_css_selector("div[id='playtime']").click()
    driver.find_element_by_css_selector("div[id='basic']").click()
    driver.find_element_by_css_selector("div[id='advanced']").click()
    driver.find_element_by_css_selector("div[id='setpiece']").click()
    driver.find_element_by_css_selector("div[id='goalie']").click()

    # iterate over seasons and match weeks
    for year in range(2017, 2019):
        for week in range(38, 39):
            submit_play_week(year, week)
            rename_file(f"{fb.get_user_directory()}Downloads\\rotowire-stats.csv", league_dict[league], year, week, player_extract)

    # unclick league if player extract
    if player_extract:
        driver.find_element_by_css_selector(f"div[data-name='{league}']").click()
    

"""
Submits a query for the specified play week
---
Parameters:
    season - season to get data for
    week - play week to get data for
"""
def submit_play_week(season, week):
    
    # select play week
    select = Select(driver.find_element_by_id("season"))
    select.select_by_value('{}'.format(season))

    select = Select(driver.find_element_by_id("start"))
    select.select_by_value('{}'.format(week))

    select = Select(driver.find_element_by_id("end"))
    select.select_by_value('{}'.format(week))

    # submit query
    driver.find_element_by_css_selector("button[class='btn outline size-1 pad-1 bold flat']").click()
    time.sleep(2)

    # download csv
    driver.find_element_by_css_selector("button[class='export-button is-csv']").click()
    time.sleep(1)


"""
Method to move the downloaded stats file to the correct location
---
Parameters:
    file_name - name of the rotowire stats csv
    league - league to save data to
    season - season of data
    week - week of the season the files corresponds to
    player_extract - boolean of whether this is player or team data
"""
def rename_file(file_name, league, season, week, player_extract):
    
    switch = True
    extract_type = "Players" if player_extract else "Teams"

    # need to wait until file is finished downloading
    while switch:
        if os.path.exists(file_name):

            # make sure there's data
            with open(file_name, "r") as fp:
                if len(fp.readlines()) < 2:
                    fp.close()
                    os.remove(f"{fb.get_user_directory()}Downloads\\rotowire-stats.csv")
                    break

            # get rid of an existing file since os.rename cannot overwrite
            if os.path.exists(f"{fb.get_directory()}Seasons\\{season}\\Rotowire\\{league}\\{extract_type}\\week{week}.csv"):
                os.remove(f"{fb.get_directory()}Seasons\\{season}\\Rotowire\\{league}\\{extract_type}\\week{week}.csv")
                
            time.sleep(1)

            # rename stats file
            os.rename(f"{fb.get_user_directory()}\\Downloads\\rotowire-stats.csv",
                f"{fb.get_directory()}Seasons\\{season}\\Rotowire\\{league}\\{extract_type}\\week{week}.csv")
            
            switch = False

        time.sleep(1)


# if there is already a rotowire download clean up
if os.path.exists(f"{fb.get_user_directory()}Downloads\\rotowire-stats.csv"):
    os.remove(f"{fb.get_user_directory()}Downloads\\rotowire-stats.csv")

# store webdriver in documents folder
driver = webdriver.Edge(f"{fb.get_user_directory()}Documents\\msedgedriver.exe")
login()

# player data
[download_csvs(league, True) for league in league_dict.keys()]

# teams data
[download_csvs(league, False) for league in league_dict.keys()]