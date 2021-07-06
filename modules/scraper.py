import requests
import json
import random
import os
import time

from googlesearch import search
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from modules.utils.misc import write_json, return_timeframe_index, format_date, convert_to_gmt

class WebScraper:
    def __init__(self):
        self.OS_PATH = os.environ.get("OS_PATH")
        self.stockLocation = f'{self.OS_PATH}/modules/utils/stockSymbols.json'
        with open(self.stockLocation, 'r') as f:
            self.updatedSymbols = json.load(f)['stockSymbols']

        self.driverPath = f'{self.OS_PATH}/chromedriver.exe'
        self.url = 'https://www.tradingview.com/symbols/'
    
    def random_stock(self):
        listOfSymbols = self.updatedSymbols
        randomSymbol = random.choice(listOfSymbols)
        urlLink = self.url + randomSymbol
        return urlLink

    def analyse_stock(self, symbol, timeframe):
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument(f'user-agent={str(UserAgent().random)}')   # Fake agent to bypass detections
        options.add_argument('--window-size=1920,1080')
        driver = webdriver.Chrome(self.driverPath, options=options)
        driver.maximize_window()
        driver.get(self.url + f'{symbol}')
        analysisResult = {}

        try:
            # First page load
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'tv-tabs__scroll-box')))
            technicalTabButtons = driver.find_element_by_class_name('tv-tabs__scroll-box').find_elements_by_class_name('tv-tabs__tab')     # Selects last tab
            technicalTabButtons[-1].click()
            
            if not timeframe == '1Day':
                # Clicks into specified timeframe
                WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="tabsRow-3jmiyUeS tabs-1LGqoVz6"')))
                timeFrameButtons = driver.find_elements_by_css_selector('div[class="tab-B2mArR2X tab-1Yr0rq0J noBorder-oc3HwerO"')
                index = return_timeframe_index(timeframe)
                timeFrameButtons[index].click()
                print(timeFrameButtons[index].text)
            
            # Retrieving stock name
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'speedometersContainer-1EFQq-4i')))
            time.sleep(0.5)     # Ensure that data is loaded prior to scraping
            stockName = driver.find_element_by_css_selector('div[class="tv-symbol-header__first-line"]').text 
            stockPrice = driver.find_element_by_css_selector('div[class="tv-symbol-price-quote__value js-symbol-last"]').text
            priceChange = driver.find_element_by_css_selector('span[class="js-symbol-change-pt tv-symbol-price-quote__change-value"]').text.strip('()')
            peRatio = driver.find_element_by_xpath('//*[@id="anchor-page-1"]/div/div[3]/div[3]/div[5]/div[1]').text
            data = {
                'Name' : f'{stockName}',
                'Price' : f'${stockPrice}',
                'Price Change' : f'{priceChange}',
                'P/E Ratio' : f'{peRatio}'
            }
            analysisResult.update(data)

            time.sleep(0.5)     # Ensure that data is loaded prior to scraping
            
            WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'tablesWrapper-3-2f1vZg')))

            oscillators = driver.find_elements_by_css_selector('tr[class="row-3rEbNObt"]')[0]
            rsiElement = oscillators.find_elements_by_class_name('cell-5XzWwbDG')
            movingAverages = driver.find_elements_by_css_selector('div[class="speedometerWrapper-1SNrYKXY"]')[-1]
            maData = movingAverages.find_elements(By.TAG_NAME, 'span')[-7:]
            # macdElement = oscillators[6].find_elements_by_class_name('cell-5XzWwbDG')
            # ema20Element = oscillators[15].find_elements_by_class_name('cell-5XzWwbDG')
            # ema50Element = oscillators[19].find_elements_by_class_name('cell-5XzWwbDG')

            data = {
                'RSI' : {
                    'Strength' : rsiElement[1].text,
                    'Decision' : rsiElement[2].text
                },
                'MA' : {
                    'Strengths' : [maData[1].text, maData[3].text, maData[5].text],
                    'Decision' : maData[0].text
                }
            }

            analysisResult.update(data)
            driver.quit()       # Gracefully exit selenium
        except Exception as e:
            write_json(repr(e))
            driver.quit()
            return 'Error'

        print(analysisResult)
        stockName = analysisResult['Name']
        currentPrice = analysisResult['Price']
        priceChange = analysisResult['Price Change']
        peRatio = analysisResult['P/E Ratio']
        rsiStrength = analysisResult['RSI']['Strength']
        rsiDecision = analysisResult['RSI']['Decision']
        maStrength = analysisResult['MA']['Strengths']
        maDecision = analysisResult['MA']['Decision']
        # macdStrength = analysisResult['MACD']['Strength']
        # macdDecision = analysisResult['MACD']['Decision']
        # ema20Strength = analysisResult['EMA20']['Strength']
        # ema20Decision = analysisResult['EMA20']['Decision']
        # ema50Strength = analysisResult['EMA50']['Strength']
        # ema50Decision = analysisResult['EMA50']['Decision']
        
        return stockName, currentPrice, priceChange, peRatio, rsiStrength, rsiDecision, maStrength, maDecision
        #macdStrength, macdDecision, ema20Strength, ema20Decision, ema50Strength, ema50Decision

    def retrieve_us_news(self, symbol):
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument(f'user-agent={str(UserAgent().random)}')   # Fake agent to bypass detections
        options.add_argument('--window-size=1920,1080')
        # options.add_argument('--disable-extensions')
        # options.add_argument('--disable-gpu')
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(self.driverPath, options=options)
        driver.maximize_window()
        driver.get(f'https://finviz.com/quote.ashx?t={symbol}')

        try:
            WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'fullview-news-outer')))

            body = driver.find_element_by_class_name('fullview-news-outer')
            subBody = body.find_elements_by_tag_name('tr')[:5]
            date = ''
            linkDict = {}

            for tr in subBody:
                if not linkDict:    # Initialise first element in dictionary
                    timeElement = tr.find_element_by_tag_name('td').text.strip().split(' ')      # Obtains date of first element
                    date = format_date(timeElement[0])
                    time = convert_to_gmt(timeElement[1])

                    element = tr.find_element_by_class_name('tab-link-news')
                    linkTitle = element.text
                    link = element.get_attribute('href')

                    data = {
                        date : [linkTitle, link, time]
                    }
                    linkDict.update(data)
                else:
                    time = tr.find_element_by_tag_name('td').text.strip()       # Remove whitespaces at the end of string
                    element = tr.find_element_by_class_name('tab-link-news')
                    linkTitle = element.text
                    link = element.get_attribute('href')
                    
                    if len(time.split(' ')) > 1:    # Checks if article belongs to previous day
                        print('Date Changed')
                        timeElement = time.split(' ')
                        date = format_date(timeElement[0])
                        time = convert_to_gmt(timeElement[1])

                        data = {
                            date : [linkTitle, link, time]
                        }
                        linkDict.update(data)
                    else:
                        linkDict[date].append(linkTitle)
                        linkDict[date].append(link)
                        linkDict[date].append(convert_to_gmt(time))
            driver.quit()       # Gracefully exit selenium

        except Exception as e:
            write_json(repr(e))
            driver.quit()
            return 'Error'

        print(linkDict)
        return linkDict

    def retrieve_sg_news(self, symbol):
        # headers = {   # Fake agent to bypass detections
        # 'User-Agent': str(UserAgent().random)}

        # googleUrl = f'https://www.google.com/search?q=sginvestors+news+{symbol}&ie=utf-8&oe=utf-8'

        # page = requests.get(googleUrl).text
        # soup = BeautifulSoup(page, 'html.parser')
        # link = soup.find_all('div', {'class':'g'})[0].find('a')['href']

        link = list(search(f"sginvestors newsrticle {symbol}", tld="com", num=5, stop=5, pause=2))[0]
        page = requests.get(link).text
        soup = BeautifulSoup(page, 'html.parser')
        articleLinks = soup.find_all('article', {'class':'stocknewsitem'})[:5]

        linkDict = {}

        try:
            for article in articleLinks:
                aClass = article.find('a')
                title = aClass['title']
                link = aClass['href']
                dateElement = article.find('div', {'class':'publisheddate'}).text.split(' ')

                if dateElement[0] in linkDict.keys():      # Checks if date already exists as a key in dictionary
                    linkDict[dateElement[0]].append(title)
                    linkDict[dateElement[0]].append(link)
                    linkDict[dateElement[0]].append(dateElement[1])
                else:
                    data = {
                        dateElement[0] : [title, link, dateElement[1]]
                    }
                    linkDict.update(data)

        except Exception as e:
            write_json(repr(e))
            return 'Error'

        print(linkDict)
        return linkDict