from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from bs4 import BeautifulSoup

# Set path to webdriver
driver_path = r'C:\Users\cadeg\Desktop\chromedriver.exe'

# chrome webdriver instance
chrome_service = ChromeService(driver_path)
driver = webdriver.Chrome(service=chrome_service)

# open nba.com team stats page
team_stats_url = 'https://www.espn.com/nba/team/stats/_/name/bos'
driver.get(team_stats_url)

driver.implicitly_wait(10)


# get html content once javascript has executed
html_content = driver.page_source

# close browser
driver.quit()

# parse html with beautifulsoup
soup = BeautifulSoup(html_content, 'html.parser')

# find all player name links
player_links = soup.find_all('a', class_='AnchorLink', attrs={'href': True, 'data-player-uid': True} )

# create set to prevent duplicate names
encountered_names = set()

for player_link in player_links:
    player_name = player_link.text.strip()
    
    # Check if the player name has not been encountered before
    if player_name not in encountered_names:
        player_url = player_link['href']
        print("Player:", player_name)
        print("Player URL:", player_url)
        print("-------------------")
        
        # Add the name to the set to avoid printing it again
        encountered_names.add(player_name)

# get all rows

rows = soup.find_all('tr', class_ = 'Table__TR')

if rows:
    # pull values out of rows
    for row in rows:
        data_cells = row.find_all('td')
        if len(data_cells) == 13:
            games_played = data_cells[0].text.strip()
            games_started = data_cells[1].text.strip()
            minutes = data_cells[2].text.strip()
            points = data_cells[3].text.strip()
            o_rebounds = data_cells[4].text.strip()
            d_rebounds = data_cells[5].text.strip()
            rebounds = data_cells[6].text.strip()
            assists = data_cells[7].text.strip()
            steals = data_cells[8].text.strip()
            blocks = data_cells[9].text.strip()
            turnovers = data_cells[10].text.strip()
            fouls = data_cells[11].text.strip()
            assist_turnover_ratio = data_cells[12].text.strip()

            print("Points:", points)
            print("Rebounds:", rebounds)
            print("Assists:", assists)
            print("-------------------")
        elif len(data_cells) == 14:
            fg_made = data_cells[0].text.strip()
            fg_attempt = data_cells[1].text.strip()
            fg_percent = data_cells[2].text.strip()
            three_made = data_cells[3].text.strip()
            three_attempt = data_cells[4].text.strip()
            three_percent = data_cells[5].text.strip()
            ft_made = data_cells[6].text.strip()
            ft_attempt = data_cells[7].text.strip()
            ft_percent = data_cells[8].text.strip()
            two_made = data_cells[9].text.strip()
            two_attempt = data_cells[10].text.strip()
            two_percent = data_cells[11].text.strip()
            scoring_efficiency = data_cells[12].text.strip()
            shooting_efficiency = data_cells[13].text.strip()

            print("FGM:", fg_made)
            print("SH-EFF:", shooting_efficiency)
        else:
            print("Not enough data cells for this row")

else:
    print("No table rows found on the webpage.")
