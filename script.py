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