import fbref_lib as fb
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
import time, os

def scan_for_problem_files():
    
    leagues = fb.get_league_dict().keys()
    t = time.perf_counter()

    for league in leagues:

        print(league)

        matches = fb.get_landing_zone_files(leagues=league)

        for match in matches:

            with open(match, "r", encoding="utf-8") as fp:
                
                text = fp.read().replace('<!--', '').replace('-->', '')
                try:
                    fb.parse_lake_match_file(match, text)
                except Exception:
                    with open('Fantasy_Soccer\\problems.txt', mode='a+') as failed_files:
                        failed_files.write(f"{match}\n")

        print(f"Execution took: {(time.perf_counter() - t)/60} min")
        t = time.perf_counter()


def repull_problem_files():
    with open('Fantasy_Soccer\\problems.txt', mode='r') as failed_files:
        for line in failed_files:
            line_split = line.strip().split("\\")
            year = line_split[7]
            league = line_split[9]
            link = "/" + line_split[-1].replace("_", "/").replace(".html", "")

            with open(line.strip(), "r", encoding="utf-8") as fp:
                fb.save_match_file(link, year, league)
                time.sleep(3)


def clean_problem_files():

    problem_types = {
        'match_awarded': [],
        'preliminary_round': [],
        'qualifying_round': []
    }

    driver = webdriver.Firefox(
        executable_path=f'{fb.get_directory()}\\Testing\\webdriver\\geckodriver.exe',
        firefox_binary=FirefoxBinary()
    )
    
    with open('Fantasy_Soccer\\problems.txt', mode='r') as failed_files:
        for line in failed_files:

            driver.get(line)

            if '*Match awarded' in driver.find_element(By.XPATH, '/html/body/div[2]/div[5]/div[2]/div[3]/div[4]').text:
                os.remove(line.strip())

            elif 'Preliminary round' in driver.find_element(By.XPATH, '/html/body/div[2]/div[5]/div[1]').text:
                os.remove(line.strip())

            elif 'Extra preliminary round' in driver.find_element(By.XPATH, '/html/body/div[2]/div[5]/div[1]').text:
                os.remove(line.strip())

            elif 'qualifying' in driver.find_element(By.XPATH, '/html/body/div[2]/div[5]/div[1]').text:
                os.remove(line.strip())
            
            elif 'Copa del Rey (First round' in driver.find_element(By.XPATH, '/html/body/div[2]/div[5]/div[1]').text:
                os.remove(line.strip())

            elif 'Copa del Rey (Second round' in driver.find_element(By.XPATH, '/html/body/div[2]/div[5]/div[1]').text:
                os.remove(line.strip())

            elif 'Coupe de France (Seventh round' in driver.find_element(By.XPATH, '/html/body/div[2]/div[5]/div[1]').text:
                os.remove(line.strip())

            else:
                print(line.strip())

scan_for_problem_files()