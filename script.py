from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from bs4 import BeautifulSoup

# Set the path to your Edge WebDriver executable
driver_path = r'C:\Users\cadeg\Desktop\chromedriver.exe'

# Create a Microsoft Edge webdriver instance
edge_service = ChromeService(driver_path)
driver = webdriver.Chrome(service=edge_service)

# Open NBA.com team stats page for the Boston Celtics
team_stats_url = 'https://www.espn.com/nba/team/stats/_/name/bos'
driver.get(team_stats_url)

driver.implicitly_wait(10)
# Get the updated HTML content after JavaScript execution
html_content = driver.page_source

# Close the browser
driver.quit()

# Parse HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

