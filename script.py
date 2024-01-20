from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
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

# Set path to webdriver
driver_path = r'C:\Users\cadeg\Desktop\chromedriver.exe'

# Chrome webdriver instance
chrome_service = ChromeService(driver_path)
driver = webdriver.Chrome(service=chrome_service)

# NBA.com URL for teams
teams_url = 'https://www.nba.com/stats/teams'

driver.get(teams_url)

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

        # Get HTML content once JavaScript has executed
    team_html_content = driver.page_source

        # Parse HTML with BeautifulSoup for player names
    team_soup = BeautifulSoup(team_html_content, 'html.parser')
    player_links = team_soup.find_all('a', class_='Anchor_anchor__cSc3P', attrs={'href': lambda x: x and '/stats/player/' in x})

    for player_link in player_links:
        player_name = player_link.text.strip()
        player_url = 'https://www.nba.com' + player_link['href'] + 'profile'

            # Navigate to the player's page
        driver.get(player_url)

            # Add appropriate waiting mechanisms (implicit/explicit waits) to ensure page loads
        time.sleep(1)  # Example: Wait for 5 seconds

            # Get HTML content once JavaScript has executed
        player_html_content = driver.page_source

            # Parse HTML with BeautifulSoup for player details
        player_soup = BeautifulSoup(player_html_content, 'html.parser')

        try:
            # Extract information using specific classes
                player_info_values = player_soup.find_all('p', class_='PlayerSummary_playerInfoValue__JS8_v')
                height = player_info_values[0].text.strip()
                weight = player_info_values[1].text.strip()
                college = player_info_values[3].text.strip()
                print(college)
                age = player_info_values[4].text.strip()[:-5]
                draft_selection = player_info_values[6].text.strip()
                experience = player_info_values[7].text.strip()[:-5]



                main_inner_info = player_soup.find('p', class_='PlayerSummary_mainInnerInfo__jv3LO')
                if main_inner_info:
                    main_inner_info_pieces = main_inner_info.text.strip().split('|')
                    print(main_inner_info_pieces)
                    team = main_inner_info_pieces[0].strip()
                    number = main_inner_info_pieces[1].replace('#', '').strip()
                    position = main_inner_info_pieces[2].strip()

                    print(f"Player: {player_name}, Team: {team}, Number: {number}, Position: {position}")

                    cursor.execute("""
                    INSERT INTO Players (player_name, player_height, player_weight, former_university, player_age, draft_selection, years_of_experience, player_team, player_number, player_position)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (player_name, height, weight, college, age, draft_selection, experience, team, number, position))

        except Exception as e:
                print(f"An error occured: {e}")
                height, weight, college, age, draft_selection, experience = '', '', '', '', '', ''


        # Extract main inner information


            # Insert player details into the database
        

# Commit changes and close connections
conn.commit()
conn.close()

# Close the browser
driver.quit()