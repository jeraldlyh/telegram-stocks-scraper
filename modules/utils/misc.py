import json
import pytz
import os

from datetime import datetime

OS_PATH = os.environ.get("OS_PATH")
textFile = f'{OS_PATH}/modules/utils/keywords.txt'

def write_json(data):
    fileLocation = f'{OS_PATH}/modules/utils/errors.json'
    with open(fileLocation, 'r') as f:
        errorDict = json.load(f)
        
    with open(fileLocation, 'w') as f:
        date = datetime.now(tz=pytz.timezone('Asia/Singapore')).strftime("%d/%m/%y")
        time = datetime.now(tz=pytz.timezone('Asia/Singapore')).strftime("GMT+8 %I:%M%p")
        errorMessage = {
            'date' : f'{date}',
            'time' : f'{time}',
            'message' : f'{data}'
        }
        errorDict['errorMessages'].append(errorMessage)
        json.dump(errorDict, f, indent=4)

def add_keyword(data):
    with open(textFile, 'r+') as f:
        keywordList = [x.rstrip('\n') for x in f.readlines()]
        if ' ' in str(data):
            word = data.replace(' ', '(.?)')
        else:
            word = data
        keywordList.append(word)
        f.seek(0)
        f.truncate()
        for x in keywordList:
            f.write(x+'\n')
        f.close()

def remove_keyword(data):
    with open(textFile, 'r+') as f:
        keywordList = [x.rstrip('\n') for x in f.readlines()]
        keywordList.remove(str(data))
        f.seek(0)
        f.truncate()
        for x in keywordList:
            f.write(x+'\n')
        f.close()

def display_keywords():
    with open(textFile, 'r+') as f:
        keywordList = [x.rstrip('\n') for x in f.readlines()]
        updatedList = []
        for word in keywordList:
            if '(.?)' in word:
                updatedList.append(word.replace('(.?)', ' '))
            else:
                updatedList.append(word)
    return updatedList

def check_strength(signalList):
    sellStrength = int(signalList[0])
    neutralStrength = int(signalList[1])
    buyStrength = int(signalList[2])
    positiveStrength = 0
    if buyStrength > sellStrength:
        positiveStrength = buyStrength
    elif sellStrength > buyStrength:
        positiveStrength = sellStrength
    else:
        positiveStrength = neutralStrength
    totalPower = sum(int(x) for x in signalList)
    strengthPower = f'{((positiveStrength / totalPower) * 100):.2f}%'
    return strengthPower

def beautify_emoji(signalDecision):
    if signalDecision.lower() == 'buy':
        return f'🟢 {signalDecision.upper()}'
    elif signalDecision.lower() == 'strong buy':
        return f'🟡 {signalDecision.upper()}'
    elif signalDecision.lower() == 'sell':
        return f'🔴 {signalDecision.upper()}'
    elif signalDecision.lower() == 'strong sell':
        return f'⚫ {signalDecision.upper()}'
    elif signalDecision.lower() == 'neutral':
        return f'⚪ {signalDecision.upper()}'

def return_timeframe_index(timeframe):
    data = {
        '1Min' : 0,
        '5Mins' : 1,
        '15Mins' : 2,
        '1Hour' : 3,
        '4Hours' : 4,
        '1Week' : 5,
        '1Month' : 6
    }
    return data[timeframe]

def format_date(date):  # Takes in date format: Oct-23-20
    dateList = date.split('-')
    # print(dateList)
    newDate = f'{dateList[1]} {dateList[0]} {dateList[2]}'
    return newDate

def decrease_day(date): # Takes in date format: 23 Oct 20
    dateList = date.split(' ')
    newDate = f'{int(dateList[0]) - 1} {dateList[1]} {dateList[2]}'
    return newDate

def convert_to_gmt(date):
    # eastern = pytz.timezone('America/New_York')
    # local = pytz.timezone('Asia/Singapore')
    # updatedDate = datetime.strptime(date, '%I:%M%p')
    # return updatedDate.replace(tzinfo=eastern).astimezone(local).strftime('%I:%M%p')
    if date[-2:] == 'AM':
        temp = list(date)
        temp[5] = 'P'
        date = ''.join(temp)
    else:
        temp = list(date)
        temp[5] = 'A'
        date = ''.join(temp)
    return date