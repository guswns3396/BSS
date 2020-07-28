import requests
from bs4 import BeautifulSoup
import code.Player as Player

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

def extractTeams():
    """
    extracts teams from baseball reference
    :return: list of Team objects
    """
    teams = []
    endpoint = '/teams/'
    page = requests.get(URL + endpoint)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.select("#teams_active tbody td[data-stat='franchise_name'] a")
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
        results = soup.select("#team_batting tbody td[data-stat='player'] a")
        for result in results:
            team.batting.append(Member(result.string, result['href']))
        # get pitching roster
        results = soup.select("#team_pitching tbody td[data-stat='player'] a")
        for result in results:
            team.pitching.append(Member(result.string, result['href']))

def extractData(teams):
    """
    extracts necessary data from website to instantiate Player objects
    :param teams: list of Team objects
    :return: lists of Hitter & Pitcher objects
    """
    hitters, pitchers = [], []
    for team in teams:
        for member in team.batting:
            # extract necessary data
            page = requests.get(URL + member.endpoint)
            soup = BeautifulSoup(page.content, 'html.parser')
            a = soup.find("a", string="162 Game Avg.")
            th = a.find_parent("th")
            # TODO: identify all necessary data
            plate_appearance = th.find_next_sibling(attrs={"data-stat": "PA"})
            hits = th.find_next_sibling(attrs={"data-stat": "H"})
            hpa = int(hits.string) / int(plate_appearance.string)
            rhp = 0
            lhp = 0
            pow = 0
            avg = 0
            fin = 0
            gro = 0
            fly = 0
            hme = 0
            awy = 0
            # instantiate hitter & add to list
            hitter = Player.Hitter(member.name,hpa,rhp,lhp,pow,avg,fin,gro,fly,hme,awy)
            hitters.append(hitter)
        for member in team.pitching:
            page = requests.get(URL + member.endpoint)
            soup = BeautifulSoup(page.content, 'html.parser')
            a = soup.find("a", string="162 Game Avg.")
            th = a.find_parent("th")
            # TODO: identify all necessary data
            innings_pitched = th.find_next_sibling(attrs={"data-stat": "IP"})
            hits = th.find_next_sibling(attrs={"data-stat": "H"})
            rhb = int(hits.string) / float(innings_pitched.string)
            lhb = int(hits.string) / float(innings_pitched.string)
            # instantiate pitcher & add to list
            pitcher = Player.Pitcher(member.name, rhb, lhb)
            pitchers.append(pitcher)
    return hitters, pitchers

if __name__ == "__main__":
    teams = extractTeams()
    extractRoster(teams)
    hitters, pitchers = extractData(teams)
