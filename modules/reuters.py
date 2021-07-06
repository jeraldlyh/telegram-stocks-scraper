import requests
import json
import datetime
import pytz
import re
import os

from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from modules.utils.misc import write_json, return_timeframe_index, format_date, convert_to_gmt

OS_PATH = os.environ.get("OS_PATH")

class Reuters:
    def __init__(self):
        self.keywordLocation = f'{OS_PATH}/modules/utils/keywords.txt'
        with open(self.keywordLocation, 'r') as f:
            self.keywords = [x.rstrip('\n') for x in f.readlines()]
            
        self.industry = ['finance/markets/us']#, 'finance/markets/asia', 'finance/markets/europe']
        self.sentLinks = {}

    def get_stocks_url(self):
        stockLinks = []

        for industry in self.industry:
            url = f'https://www.reuters.com/{industry}'
            try:
                page = requests.get(url).text
                soup = BeautifulSoup(page, 'html.parser')
                headlines = soup.find_all('div', {'class' : 'story-content'})
                dateToday = datetime.datetime.now(tz=pytz.timezone('Asia/Singapore')).strftime("%b").lower()

                for headline in headlines:
                    dateToCheck = headline.find('span', {'class' : 'timestamp'}).text.lower()
                    if dateToday in dateToCheck:    # Checks if the article is dated yesterday
                        continue
                    else:
                        individualTag = headline.find('a')['href']
                        link = f'https://www.reuters.com{individualTag}'
                        stockLinks.append(link)
            except Exception as e:
                write_json(repr(e))
                
        return stockLinks

    def analyse_url(self):
        updatedStockLinks = {}
        linkList = self.get_stocks_url()
        # print(linkList)
        headers = {   # Fake agent to bypass detections
        'User-Agent': str(UserAgent().random)}

        for link in linkList:
            if link in updatedStockLinks or link in self.sentLinks:   # Checks if link exists in list and goes to next
                continue
            else:
                for keyword in self.keywords:
                    if link in updatedStockLinks or link in self.sentLinks:   # Breaks so that it does not rerun keyword search in PARAGRAPHS
                        break

                    # Search for exact matches in URL
                    match = re.search(r'\b{0}\b'.format(keyword), link, flags=re.IGNORECASE)
                    if match:
                        updatedStockLinks.update({link : match.group(0)})
                        print(f'Found in URL - {link}')
                        break

                    # Checks if keywords are located in body text of article
                    page = requests.get(link, headers=headers).text
                    soup = BeautifulSoup(page, 'html.parser')

                    # HTML tag for body paragraph of article
                    paragraphs = soup.find_all('p', {'class' : 'Paragraph-paragraph-2Bgue ArticleBody-para-TD_9x'})
                    for sentences in paragraphs:
                        if link in updatedStockLinks or link in self.sentLinks:   # Breaks so that it does not rerun keyword search in SENTENCE
                            break

                        match = re.search(r'\b{0}\b'.format(keyword), sentences.text, flags=re.IGNORECASE)
                        if match:
                            updatedStockLinks.update({link : match.group(0)})
                            print(f'Found in website itself- {link}')
                            break                                     

        if updatedStockLinks:       # If there are new updates that just got sent, update sentLinks
            for link in updatedStockLinks:
                self.sentLinks[link] = updatedStockLinks[link]      # Updates sentLinks with updatedLinks to prevent duplicates in future
        return updatedStockLinks