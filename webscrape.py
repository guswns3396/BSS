import requests
from bs4 import BeautifulSoup

YEAR = 2020

# define team class
class Team:
    def __init__(self, name, endpoint):
        """
        instantiate team class
        batting: list of batting Player objects
        pitching: list of pitching Player objects
        :param name: name of team
        :param endpoint: endpoint of team on website
        """
        self.name = name
        self.endpoint = endpoint
        self.batting = []
        self.pitching = []
# define Member class
class Member:
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
for team in teams:
    print(team.name)
    page = requests.get(URL + team.endpoint + str(YEAR) + ".shtml")
    soup = BeautifulSoup(page.content, 'html.parser')
    # get batting roster
    results = soup.select("#team_batting tbody tr a")
    for result in results:
        team.batting.append(Member(result.string, result['href']))
    # get pitching roster
    results = soup.select("#team_pitching tbody tr a")
    for result in results:
        team.pitching.append(Member(result.string, result['href']))

#