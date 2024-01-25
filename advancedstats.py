from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import mysql.connector
import time

# Connect to the database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Edgerunner77",
    database="basketball"
)

cursor = conn.cursor()

cursor.execute("Select player_name from players join advancedstats on players.player_id = advancedstats.player_id WHERE offensive_rating <= 5")

result_of_name_search = cursor.fetchall()

# Set path to webdriver
driver_path = r'C:\Users\cadeg\Desktop\chromedriver.exe'

# Chrome webdriver instance
chrome_service = ChromeService(driver_path)
driver = webdriver.Chrome(service=chrome_service)

# NBA.com URL for teams
teams_url = 'https://www.nba.com/stats/teams'

driver.get(teams_url)

# Add appropriate waiting mechanisms (implicit/explicit waits) to ensure page loads
time.sleep(3) 

driver.implicitly_wait(30)

# Get HTML content once JavaScript has executed
html_content = driver.page_source

# Parse HTML with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find links to each team's page
team_links = soup.find_all('a', class_='Anchor_anchor__cSc3P StatsTeamsList_teamLink__q_miK')

                                        
for team_link in team_links:
    # Extract team name and URL
    team_name = team_link.text.strip()

    team_url = 'https://www.nba.com' + team_link['href']

    # Navigate to the team's page
    driver.get(team_url)
    

    # Add appropriate waiting mechanisms (implicit/explicit waits) to ensure page loads
    time.sleep(1)  

        # Get HTML content once JavaScript has executed
    team_html_content = driver.page_source

        # Parse HTML with BeautifulSoup for player names
    team_soup = BeautifulSoup(team_html_content, 'html.parser')
    player_links = team_soup.find_all('a', class_='Anchor_anchor__cSc3P', attrs={'href': lambda x: x and '/stats/player/' in x})

    for player_link in player_links:
        player_name = player_link.text.strip()

        player_names_from_search = [row[0] for row in result_of_name_search]
        if player_name in player_names_from_search:

            player_url = 'https://www.nba.com' + player_link['href'] + 'profile'
            # Navigate to the player's page
            driver.get(player_url)

            
                # Add appropriate waiting mechanisms (implicit/explicit waits) to ensure page loads
            time.sleep(1)

             # Wait for the dropdown to be clickable
            dropdown_menu = WebDriverWait(driver, 80).until(
                EC.element_to_be_clickable((By.XPATH, '(//select[@class="DropDown_select__4pIg9"])[1]'))
            )

            # Click the dropdown to open the options
            dropdown_menu.click()

            # Wait for the "Regular Season" option to be clickable
            regular_season_option = WebDriverWait(driver, 85).until(
                EC.element_to_be_clickable((By.XPATH, '(//option[@value="Regular Season"])'))
            )

            # Click the "Regular Season" option
            regular_season_option.click()


            dropdown_menu_two = WebDriverWait(driver, 85).until(
                EC.element_to_be_clickable((By.XPATH, '(//select[@class="DropDown_select__4pIg9"])[2]'))
            )

            # Click the dropdown to open the options
            dropdown_menu_two.click()

            # Wait for the "Regular Season" option to be clickable
            mode_option = WebDriverWait(driver, 85).until(
                EC.element_to_be_clickable((By.XPATH, '(//option[@value="PerGame"])'))
            )

            mode_option.click()



            # Get HTML content once JavaScript has executed
            player_html_content = driver.page_source

            # Parse HTML with BeautifulSoup for player details
            player_soup = BeautifulSoup(player_html_content, 'html.parser')
            try:
                        time.sleep(2)
                        driver.implicitly_wait(10)
                    # Extract information using specific classes
                        stat_table = player_soup.find_all('tbody', class_ = 'Crom_body__UYOcU')
                        table2 = stat_table[1]
                        if table2:
                                    rows = table2.find('tr')
                                    stats = rows.find_all('td')
                                    if stats:
                                
                                        offensive_rating = stats[4].text.strip()
                                        defensive_rating = stats[5].text.strip()
                                        net_rating = stats[6].text.strip()
                                        assist_percent = stats[7].text.strip()
                                        assist_turnover = stats[8].text.strip()
                                        assist_ratio = stats[9].text.strip()
                                        o_rebound_percent = stats[10].text.strip()
                                        d_rebound_percent = stats[11].text.strip()
                                        rebound_percent = stats[12].text.strip()
                                        turnover_ratio = stats[13].text.strip()
                                        effective_fg_percent = stats[14].text.strip()
                                        true_shooting = stats[15].text.strip()
                                        usage = stats[16].text.strip()
                                        pace = stats[17].text.strip()
                                        total_impact = stats[18].text.strip()

                                        print(player_name)

                                        insert_query = """
                                        UPDATE AdvancedStats INNER JOIN players ON players.player_id = advancedstats.player_id SET players.player_id = advancedstats.player_id,
                                            offensive_rating = %s, defensive_rating = %s, net_rating = %s, assist_percent =%s, assist_turnover  = %s, assist_ratio  = %s, 
                                            o_rebound_percent = %s, d_rebound_percent = %s, rebound_percent = %s, turnover_ratio = %s, effective_fg_percent = %s,
                                            true_shooting = %s, usage_rate = %s, pace = %s, total_impact  = %s where player_name = %s
                                            """

                                        values = (
                                            offensive_rating, defensive_rating, net_rating, assist_percent, assist_turnover, assist_ratio, 
                                            o_rebound_percent, d_rebound_percent, rebound_percent, turnover_ratio, effective_fg_percent,
                                            true_shooting, usage, pace, total_impact, player_name
                                        )
                                        cursor.execute(insert_query, values)
                                        print(f"Inserted data for {player_name}")   
                                    
                                    else:
                                            print(f"No 'td' elements found for {player_name}")
                                            def error():
                                                    
                                                offensive_rating, defensive_rating, net_rating, assist_percent, assist_turnover, assist_ratio, \
                                                o_rebound_percent, d_rebound_percent, rebound_percent, turnover_ratio, effective_fg_percent, \
                                                true_shooting, usage, pace, total_impact = [0] * 15

                                                insert_query = """
                                                UPDATE AdvancedStats INNER JOIN players ON players.player_id = advancedstats.player_id SET players.player_id = advancedstats.player_id,
                                                    offensive_rating = %s, defensive_rating = %s, net_rating = %s, assist_percent =%s, assist_turnover  = %s, assist_ratio  = %s, 
                                                    o_rebound_percent = %s, d_rebound_percent = %s, rebound_percent = %s, turnover_ratio = %s, effective_fg_percent = %s,
                                                    true_shooting = %s, usage_rate = %s, pace = %s, total_impact  = %s where player_name = %s
                                                    """


                                                values = (
                                                offensive_rating, defensive_rating, net_rating, assist_percent, assist_turnover, assist_ratio, 
                                                o_rebound_percent, d_rebound_percent, rebound_percent, turnover_ratio, effective_fg_percent,
                                                true_shooting, usage, pace, total_impact, player_name
                                            )
                                                cursor.execute(insert_query, values)
                                                print(f"Second try, inserted data for {player_name}") 


                        else:
                            print(f"Table body with class 'Crom_body__UYOcU' not found for {player_name}")
                            error()

            except Exception as e:
                print(f"An error occured: {e}")
                error()
        

conn.commit()
conn.close()

driver.quit()