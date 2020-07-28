import requests
from bs4 import BeautifulSoup

URL = 'https://www.baseball-reference.com'
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
def extractTeams():
    """
    extracts teams from baseball reference
    :return: list of Team objects
    """
    teams = []
    endpoint = '/teams/'
    page = requests.get(URL + endpoint)
    soup = BeautifulSoup(page.content, 'html.parser')
    # list of tr tags that are under tbody of table with id="teams_active"
    trs = soup.select("#teams_active tbody tr")
    # list of a tags under td that have attribute data-stat='franchise_name'
    results = soup.select("td[data-stat='franchise_name'] a")
    for result in results:
        teams.append(Team(result.string,result['href']))
    return teams

def extractRoster(teams):
    """
    extracts batting & pitching roster for each team in list
    :param teams: list of Team objects
    :return: list of Team objects
    """
    # get roster for each team
    for team in teams:
        page = requests.get(URL + team.endpoint + str(YEAR) + ".shtml")
        soup = BeautifulSoup(page.content, 'html.parser')
        # get batting roster
        results = soup.select("#team_batting tbody tr td:nth-of-type(3) a")
        for result in results:
            team.batting.append(Member(result.string, result['href']))
        # get pitching roster
        results = soup.select("#team_pitching tbody tr a")
        for result in results:
            team.pitching.append(Member(result.string, result['href']))
    return teams

# for each player, gather necessary data
def extractData(teams):
    for team in teams:
        for hitter in team.batting:
            page = requests.get(URL + hitter.endpoint)
            soup = BeautifulSoup(page.content, 'html.parser')
            results = soup.select("#batting_standard tfoot tr th", string="162 Game Avg.")
            for result in results:
                print(result)

if __name__ == "__main__":
    teams = extractTeams()
    teams = extractRoster(teams)
    extractData(teams)