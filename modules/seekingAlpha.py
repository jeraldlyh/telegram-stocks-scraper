import requests
import os
import re

from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from selenium import webdriver
from modules.utils.misc import write_json, return_timeframe_index, format_date, convert_to_gmt

OS_PATH = os.environ.get("OS_PATH")

class SeekingAlpha:
    def __init__(self):
        self.keywordLocation = f'{OS_PATH}/modules/utils/keywords.txt'
        with open(self.keywordLocation, 'r') as f:
            self.keywords = [x.rstrip('\n') for x in f.readlines()]
        
        self.driverPath = f'{OS_PATH}/chromedriver.exe'
        self.sentLinks = {}

    def get_stocks_url(self):
        stockLinks = []

        url = 'https://seekingalpha.com/market-news'
        page = requests.get(url).text
        soup = BeautifulSoup(page, 'html.parser')
        headlines = soup.find_all('li', {'class' : 'item'})
        for headline in headlines:
            try:
                individualTag = headline.find('a')['href']
                link = f'https://seekingalpha.com{individualTag}'
                stockLinks.append(link)
            except Exception:
                continue
                
        return stockLinks

    def analyse_url(self):
        options = webdriver.ChromeOptions()
        options.headless = False
        options.add_argument(f'user-agent={str(UserAgent().random)}')   # Fake agent to bypass detections
        options.add_argument('--window-size=1920,1080')
        driver = webdriver.Chrome(self.driverPath, options=options)
        driver.maximize_window()

        updatedStockLinks = {}
        linkList = self.get_stocks_url()
        # print(linkList)

        for link in linkList:
            if link in updatedStockLinks or link in self.sentLinks:   # Checks if link exists in list and goes to next
                continue
            else:
                driver.get(link)
                for keyword in self.keywords:
                    if link in updatedStockLinks or link in self.sentLinks:   # Breaks so that it does not rerun keyword search since the link has already been added
                        break

                    match = re.search(r'\b{0}\b'.format(keyword), link, flags=re.IGNORECASE)
                    if match:   # Checks if keyword is located in url which often is the header
                        updatedStockLinks.update({link : match.group(0)})
                        print(f'Found in URL - {link}')
                        break

                    # Checks if keywords are located in body text of article
                    try:
                        # Chunk of sentences contained in a paragraph string
                        paragraph = driver.find_element_by_class_name('__559fe-pTT3d').text

                        # TODO ADD WEBDRIVERWAIT

                        match = re.search(r'\b{0}\b'.format(keyword), paragraph, flags=re.IGNORECASE)
                        if match:
                            updatedStockLinks.update({link : match.group(0)})
                            print(f'Found in website itself- {link}')
                            break
                    except:     # If page is unable to load, proceed to next
                        continue

        driver.quit()       # Gracefully exit selenium

        if updatedStockLinks:       # If there are new updates that just got sent, update sentLinks
            for link in updatedStockLinks:
                self.sentLinks[link] = updatedStockLinks[link]      # Updates sentLinks with updatedLinks to prevent duplicates in future
        return updatedStockLinks