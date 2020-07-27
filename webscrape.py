import requests
from bs4 import BeautifulSoup

# define team class
class Team:
    def __init__(self, name, endpoint):
        self.name = name
        self.endpoint = endpoint

# make GET request to URL to get static page
URL = 'https://www.baseball-reference.com'
endpoint = '/teams/'
page = requests.get(URL + endpoint)

# instantiate soup using html content
soup = BeautifulSoup(page.content, 'html.parser')

# extract teams
teams = []
results = soup.select("td[data-stat='franchise_name'] a")
for result in results:
    teams.append(Team(result.string,result['href']))

# get roster for each team

