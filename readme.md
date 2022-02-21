# Pathe movie

Get an email notification when new movies are released at the dutch cinema pathe

- Works with the current website of www.pathe.nl, tested on February 21, 2022
- Mail is sent via mailgun

## Features

- Only receive an email with newly added movies
- Script can be run manually as well as periodically (via cron for example)
- Log is kept in case of an error during the scrape process

## Installation

Pathe scraper needs [Python3](https://www.python.org) to run.

Install the required libraries, stored in requirements.txt
Installation with pip:

```sh
pip install -r requirements.txt
```

Fill in the mailgun API variable, storen in the scrape.py file

### Used libraries

| Libratie       | Link                                             |
| -------------- | ------------------------------------------------ |
| Requests       | [https://pypi.org/project/requests/]             |
| Beautifulsoup4 | [https://pypi.org/project/beautifulsoup4/]       |

## Manual

Run scrape.py

```sh
python3 scrape.py
```

An email will be sent with new movies when they are found.

Previously sent movies will not be resent. (movies are stored in database.txt)

Are you not receiving an email? See log.txt for log messages
