##########################################################################################
# File: rotowire_scraper.py
# File Created: Wednesday, 1st September 2021 7:56:01 pm
# Author: Oliver DeBarros
# -----
# Last Modified: Wednesday, 1st September 2021 7:56:03 pm
# Modified By: Oliver DeBarros
# -----
# Description:
##########################################################################################


from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time, os

league_dict = {
    "EPL": "Premier_League",
    "LIGA": "La_Liga",
    "SERI": "Serie_A",
    "FRAN": "Ligue_1",
    "BUND": "Bundesliga"
}

creds = os.getenv("rotowire").split("|")
username = creds[0]
password = creds[1]

def login():
    driver.get("https://www.rotowire.com/users/login.php?go=%2F")
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_css_selector("button[class='btn primary full-width size-2 mb-20']").click()

def download_csvs(league):

    driver.get("https://www.rotowire.com/soccer/stats.php")

    #select the league
    driver.find_element_by_css_selector("div[data-name='{}']".format(league)).click()
    
    #select all elements
    driver.find_element_by_css_selector("div[id='playtime']").click()
    driver.find_element_by_css_selector("div[id='basic']").click()
    driver.find_element_by_css_selector("div[id='advanced']").click()
    driver.find_element_by_css_selector("div[id='setpiece']").click()
    driver.find_element_by_css_selector("div[id='goalie']").click()

    for year in [2021]:
        for week in range(9,25):
            submit_play_week(league, year, week)
    

def submit_play_week(league, season, week):
    #select play week
    select = Select(driver.find_element_by_id("season"))
    select.select_by_value('{}'.format(season))

    select = Select(driver.find_element_by_id("start"))
    select.select_by_value('{}'.format(week))

    select = Select(driver.find_element_by_id("end"))
    select.select_by_value('{}'.format(week))

    #submit query
    driver.find_element_by_css_selector("button[class='btn outline size-1 pad-1 bold flat']").click()
    time.sleep(1)

    #download csv
    driver.find_element_by_css_selector("button[class='export-button is-csv']").click()
    time.sleep(3)
    rename_file(r"C:\Users\debar\Downloads\rotowire-stats.csv", league, season, week)

    
def rename_file(file_name, league, season, week):
    
    switch = True

    while switch:
        if os.path.exists(file_name):

            os.rename(r"C:\Users\debar\Downloads\rotowire-stats.csv",
                r"C:\Users\debar\Documents\Programming\Fantasy_Soccer\Seasons\{}\Rotowire\{}\Players\week{}.csv".format(season, league_dict[league], week))
            switch = False


        time.sleep(.5)


driver = webdriver.Edge(r"C:\Users\debar\Documents\msedgedriver.exe")
login()
[download_csvs(league) for league in league_dict.keys()]