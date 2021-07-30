## Description
<div>
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/Made%20With-Python-blue.svg?style=for-the-badge&logo=Python" alt="Made with Python 3.6">
  </a>
</div>
Telegram webscraper bot that provides real-time news updates based on a set of keywords specified by users.

Information is currently being scraped from the following sources:
| Source                                         | Purpose          |
:----------------------------------------------- | :--------------: |
| [SeekingAlpha](https://seekingalpha.com/)      | News             |
| [Reuters](https://www.reuters.com/)            | News             |
| [SGinvestors.io](https://sginvestors.io/)      | News             |
| [TradingView](https://www.tradingview.com/)    | Stock Indicators |

## Features
* **Keyword-scoped Search**
  * `/add <keyword>` - Add keyword into watchlist
  * `remove <keyword>` - Removes keyword from watchlist
  * `/display` - Displays current keywords in watchlist

* **News Article Search**
  * `/news <market> <stockSymbol>` - Retrieves news for specified stock symbol (_only US/SG markets are supported_)

* **Stock Analysis**
  * `/analyse <stockSymbol>` - Analyse a specified stock symbol based on a preset indicators (_relative strength index, moving average_)

## Installation
Unfortunately, this repository is no longer maintained and developed since October, 2020. Any breaking changes/errors will not be fixed.
Nonetheless, you're able to host the telegram bot locally by setting up the necessary configs in .env file.

| Requirements             | Reference                                                                                                         |
:------------------------- | :---------------------------------------------------------------------------------------------------------------: |
| Python                   | [Installation](https://www.python.org/)                                                                           |
| Telegram Bot Token       | [Documentation](https://core.telegram.org/bots#6-botfather)                                                       |
| Telegram Chat ID         | [Reference](https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id)                 |

Clone the repo:
```console
$ git clone https://github.com/jeraldlyh/telegram-webscraper
$ cd telegram-webscraper
```

Install dependencies:
```console
$ pip3 install -r requirements.txt
```

## Screenshots
Refer to write up [here](https://alkaline-fifth-fae.notion.site/README-md-f182189145724c5591bf6b7fd7ea7eec)
