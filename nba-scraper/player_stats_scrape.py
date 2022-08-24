from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
import csv
import re

# Create an instance of Chrome WebDriver and then navigate to the NBA statistics page.
# Then, force the instance to explicitly wait in order to allow all elements to load into the DOM.
browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get('https://www.nba.com/stats/leaders/')
time.sleep(2)

# Store the number of pages within the table
num_pages_element = browser.find_element_by_xpath("/html/body/main/div/div/div[2]/div/div/nba-stat-table/div[1]/div/div").text
num_pages = int(next(re.finditer(r'\d+$', num_pages_element)).group(0))

# Record each individual player's statistics and store it in the player list
player_list = []
h = 1
j = 2
i = 1
while h <= num_pages:
    try:
        player = []
        while j <= 22:
            if j == 2:
                info = browser.find_element_by_xpath('/html/body/main/div/div/div[2]/div/div/nba-stat-table/div[2]/div[2]/table/tbody/tr[' + str(i) + ']/td[2]/a').text
            else:
                info = float(browser.find_element_by_xpath('/html/body/main/div/div/div[2]/div/div/nba-stat-table/div[2]/div[1]/table/tbody/tr[' + str(i) + ']/td[' + str(j) + ']').text)
            player.append(info)
            j = j + 1
        player_list.append(player)
        j = 2
        i = i + 1
    except:
        element = browser.find_element_by_xpath("//a[@class='stats-table-pagination__next']")
        browser.execute_script("arguments[0].click();", element)
        # element.click()
        i = 1
        j = 2
        h = h + 1
        continue
browser.close()

# Write the header and player statistics to a CSV file
headerRow = ['Player', 'GP', 'MIN', 'PTS', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%', 'FTM', 'FTA', 'FT%', 'OREB', 'DREB',
             'REB', 'AST', 'STL', 'BLK', 'TOV', 'EFF']
with open('player_stats.csv', 'w+', newline='') as my_csv:
    csvWriter = csv.writer(my_csv)
    csvWriter.writerow(headerRow)
    csvWriter.writerows(player_list)

