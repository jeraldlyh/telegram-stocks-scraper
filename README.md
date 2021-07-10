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
<div align="center">
  <h4>Keyword-scoped Search</h4>
  <img src="https://s3.us-west-2.amazonaws.com/secure.notion-static.com/1ded5fba-53a1-4f6c-84ca-46d10d4a8100/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45O3KS52Y5%2F20210706%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20210706T161610Z&X-Amz-Expires=86400&X-Amz-Signature=85df9562a1d47162eb178a3516a93e024e7c0ac551c377d25324b47bad26bc6c&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22Untitled.png%22" />
  <img src="https://s3.us-west-2.amazonaws.com/secure.notion-static.com/1ded5fba-53a1-4f6c-84ca-46d10d4a8100/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45O3KS52Y5%2F20210706%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20210706T161610Z&X-Amz-Expires=86400&X-Amz-Signature=85df9562a1d47162eb178a3516a93e024e7c0ac551c377d25324b47bad26bc6c&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22Untitled.png%22" />  
  <img src="https://s3.us-west-2.amazonaws.com/secure.notion-static.com/cf230687-12ab-4acf-a400-332091b4ec4e/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45O3KS52Y5%2F20210706%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20210706T161641Z&X-Amz-Expires=86400&X-Amz-Signature=e5f07c473eff619ddbcb3a0475e2f3c5166cae0aa7b310a749b722333daf83ea&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22Untitled.png%22" />
  <img src="https://s3.us-west-2.amazonaws.com/secure.notion-static.com/2113c93a-8836-4231-b581-a42cbcf03eb8/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45O3KS52Y5%2F20210710%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20210710T161030Z&X-Amz-Expires=86400&X-Amz-Signature=75caca5eb96229eacf5e8cadd492dfc08716230b8fc6da8b79c0557cac4b6cb5&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22Untitled.png%22" />
    
   <h4>Stock Analysis</h4>
  <img src="https://s3.us-west-2.amazonaws.com/secure.notion-static.com/e9d07ad3-2d7f-40fb-b260-32d5d08d27ed/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45O3KS52Y5%2F20210706%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20210706T164311Z&X-Amz-Expires=86400&X-Amz-Signature=4ba469e724b2052a2d4ce1bd58e499d5470c47a1c747ae35a46f0d71686c43f8&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22Untitled.png%22" />
    
  <h4>News Search</h4>
  <img src="https://s3.us-west-2.amazonaws.com/secure.notion-static.com/3f108ed9-fa74-4dce-a4ae-2f783f54ecf1/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45O3KS52Y5%2F20210706%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20210706T162513Z&X-Amz-Expires=86400&X-Amz-Signature=c1b263c8c055b1ef18bc4ba457c29d94aff3731fa6758eb5e9afc4aadb5d3916&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22Untitled.png%22" />
  <img src="https://s3.us-west-2.amazonaws.com/secure.notion-static.com/207eb8e0-dcb1-4534-bdb9-e9800a80d60c/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45O3KS52Y5%2F20210706%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20210706T162514Z&X-Amz-Expires=86400&X-Amz-Signature=e0356789ea1774a63b74d1e53d0a5eeb1119039c77287628f696c0120b99eae2&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22Untitled.png%22" />
</div>
