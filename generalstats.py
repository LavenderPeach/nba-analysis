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

cursor.execute("Select player_name from players join generalstats on players.player_id = generalstats.player_id where games_played <= 6")

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
            dropdown_menu = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '(//select[@class="DropDown_select__4pIg9"])[1]'))
            )

            # Click the dropdown to open the options
            dropdown_menu.click()

            # Wait for the "Regular Season" option to be clickable
            regular_season_option = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '(//option[@value="Regular Season"])'))
            )

            # Click the "Regular Season" option
            regular_season_option.click()


            dropdown_menu_two = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '(//select[@class="DropDown_select__4pIg9"])[2]'))
            )

            # Click the dropdown to open the options
            dropdown_menu_two.click()

            # Wait for the "Regular Season" option to be clickable
            mode_option = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '(//option[@value="PerGame"])'))
            )

            mode_option.click()

            # Get HTML content once JavaScript has executed
            player_html_content = driver.page_source

            # Parse HTML with BeautifulSoup for player details
            player_soup = BeautifulSoup(player_html_content, 'html.parser')
            try:
                        time.sleep(5)
                        driver.implicitly_wait(30)
                        # Extract information using specific classes
                        stat_table = player_soup.find('tbody', class_ = 'Crom_body__UYOcU')
                        if stat_table:
                                    rows = stat_table.find_all('tr')
                                    third_row = rows[0]
                                    stats = third_row.find_all('td')
                                
                                    games_played = stats[2].text.strip()
                                    minutes = stats[3].text.strip()
                                    points = stats[4].text.strip()
                                    fg_made = stats[5].text.strip()
                                    fg_attempt = stats[6].text.strip()
                                    fg_percent = stats[7].text.strip()
                                    three_made = stats[8].text.strip()
                                    three_attempt = stats[9].text.strip()
                                    three_percent = stats[10].text.strip()
                                    ft_made = stats[11].text.strip()
                                    ft_attempt = stats[12].text.strip()
                                    ft_percent = stats[13].text.strip()
                                    o_rebounds = stats[14].text.strip()
                                    d_rebounds = stats[15].text.strip()
                                    t_rebounds = stats[16].text.strip()
                                    assists = stats[17].text.strip()
                                    turnovers = stats[18].text.strip()
                                    steals = stats[19].text.strip()
                                    blocks = stats[20].text.strip()
                                    fouls = stats[21].text.strip()
                                    dd = stats[23].text.strip() 
                                    td = stats[24].text.strip()
                                    efficiency = stats[25].text.strip()

                                    print(player_name)

                                    insert_query = """
                                        UPDATE GeneralStats INNER JOIN players ON players.player_id = generalstats.player_id SET players.player_id = generalstats.player_id,
                                        games_played = %s, minutes = %s, points = %s, field_goals_made = %s, field_goals_attempted = %s,
                                        field_goal_percentage = %s, three_point_made = %s, three_point_attempt = %s, three_point_percentage = %s,
                                        free_throw_attempts = %s, free_throw_makes = %s, free_throw_percentage = %s, offensive_rebounds = %s,
                                        defensive_rebounds = %s, total_rebounds = %s, assists = %s, turnovers = %s, steals = %s, blocks = %s,
                                        personal_fouls = %s, double_doubles = %s, triple_doubles = %s, efficiency = %s where player_name = %s
                                    
                                    """

                                    values = (
                                        games_played, minutes, points, fg_made, fg_attempt, fg_percent, three_made, three_attempt,
                                        three_percent, ft_attempt, ft_made, ft_percent, o_rebounds, d_rebounds, t_rebounds, assists, turnovers,
                                        steals, blocks, fouls, dd, td, efficiency, player_name
                                    )

                                    cursor.execute(insert_query, values)



                                    print(f"Inserted data for {player_name}")   
                                    
                        else:
                            print(f"Table body with class 'Crom_body__UYOcU' not found for {player_name}")
                            games_played, minutes, points, fg_made, fg_attempt, fg_percent, three_made, three_attempt, \
                                            three_percent, ft_attempt, ft_made, ft_percent, o_rebounds, d_rebounds, t_rebounds, assists, turnovers, \
                                            steals, blocks, fouls, dd, td, efficiency = [0] * 23

                            insert_query = """
                                        UPDATE GeneralStats INNER JOIN players ON players.player_id = generalstats.player_id SET players.player_id = generalstats.player_id,
                                        games_played = %s, minutes = %s, points = %s, field_goals_made = %s, field_goals_attempted = %s,
                                         field_goal_percentage = %s, three_point_made = %s, three_point_attempt = %s, three_point_percentage = %s,
                                        free_throw_attempts = %s, free_throw_makes = %s, free_throw_percentage = %s, offensive_rebounds = %s,
                                         defensive_rebounds = %s, total_rebounds = %s, assists = %s, turnovers = %s, steals = %s, blocks = %s,
                                        personal_fouls = %s, double_doubles = %s, triple_doubles = %s, efficiency = %s where player_name = %s
                                         
                                        """
                            values = (
                                    games_played, minutes, points, fg_made, fg_attempt, fg_percent, three_made, three_attempt,
                                    three_percent, ft_attempt, ft_made, ft_percent, o_rebounds, d_rebounds, t_rebounds, assists, turnovers,
                                    steals, blocks, fouls, dd, td, efficiency, player_name
                                    )
                            cursor.execute(insert_query, values)
                            print(f"Second try, inserted data for {player_name}")   

                                

            except Exception as e:
                print(f"An error occured: {e}")
                    

conn.commit()
conn.close()

driver.quit()
