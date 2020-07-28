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
            rhp = int(hits.string) / int(plate_appearance.string)
            lhp = 1
            pow = 2
            avg = 3
            fin = 4
            gro = 5
            fly = 6
            hme = 7
            awy = 8
            # instantiate hitter & add to list
            hitter = Player.Hitter(member.name,rhp,lhp,pow,avg,fin,gro,fly,hme,awy)
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
            lhb = 1
            # instantiate pitcher & add to list
            pitcher = Player.Pitcher(member.name, rhb, lhb)
            pitchers.append(pitcher)
    return hitters, pitchers

def exportHittersToCSV(hitters):
    """
    exports all the Hitter stats into csv
    :param hitters: list of Hitter objects
    :return: None
    """
    with open("../data/hitters.csv","w") as f:
        header = "Player Name,RHP,LHP,HPPower,HPAvg,HPFinesse,HPGroundball,HPFlyball,HPHome,HPAway"
        print(header, file=f)
        for hitter in hitters:
            data = [hitter.name,hitter.RHP,hitter.LHP,hitter.HPPower,hitter.HPAvg,
                  hitter.HPFinesse,hitter.HPGroundball,hitter.HPFlyball,
                  hitter.HPHome,hitter.HPAway]
            for i in range(len(data)):
                data[i] = str(data[i])
            print(",".join(data),file=f)

def exportPitchersToCSV(pitchers):
    """
        exports all the Pitcher stats into csv
        :param pitchers: list of Pitcher objects
        :return: None
        """
    with open("../data/pitchers.csv", "w") as f:
        header = "Player Name, RHB, LHB"
        print(header, file=f)
        for pitcher in pitchers:
            data = [pitcher.name, pitcher.RHB, pitcher.LHB]
            for i in range(len(data)):
                data[i] = str(data[i])
            print(",".join(data), file=f)

if __name__ == "__main__":
    teams = extractTeams()
    extractRoster(teams)
    hitters, pitchers = extractData(teams)
    exportHittersToCSV(hitters)
    exportPitchersToCSV(pitchers)
