import requests
from bs4 import BeautifulSoup
from bs4 import Comment
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

def searchForTable(soup, id):
    """
    searches for the table given the id of the table
    :param soup: soup object containing the page
    :param id: id of the table
    :return: soup of table if found, None if not found
    """
    table = soup.find(id=id)
    # in case data is commented out
    if table == None:
        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        id = "id=\"" + id + "\""
        for comment in comments:
            if id in comment:
                table = comment
                table = table[len("<!--"):-len("-->")].strip()
                table = BeautifulSoup(table, 'html.parser')
                return table
        # data not found even in comments:
        return None
    else:
        return table

def extractFromTable(table: BeautifulSoup, type=None):
    """
    extracts data from table depending on type
    :param table: soup object of table
    :param type: string that specifies hitter or pitcher
    :return: dictionary of data extracted
    """
    data = {}
    if type == "hitter":
        # TODO: identify all necessary data
        # in case table not found
        plate_appearance = 0
        hits = 0
        # in case table found
        if table != None:
            a = table.find("a", string="162 Game Avg.")
            th = a.find_parent("th")
            plate_appearance = int(th.find_next_sibling(attrs={"data-stat": "PA"}).string)
            hits = int(th.find_next_sibling(attrs={"data-stat": "H"}).string)
        # calculate all stats
        if plate_appearance == 0:
            data['rhp'] = 0
        else:
            data['rhp'] = hits / plate_appearance
        data['lhp'] = 1
        data['pow'] = 2
        data['avg'] = 3
        data['fin'] = 4
        data['gro'] = 5
        data['fly'] = 6
        data['hme'] = 7
        data['awy'] = 8
        return data
    elif type == "pitcher":
        # TODO: identify all necessary data
        # in case search not found
        innings_pitched = 0
        hits = 0
        # in case search found
        if table != None:
            a = table.find("a", string="162 Game Avg.")
            th = a.find_parent("th")
            innings_pitched = float(th.find_next_sibling(attrs={"data-stat": "IP"}).string)
            hits = int(th.find_next_sibling(attrs={"data-stat": "H"}).string)
        # calculate stats
        if innings_pitched == 0:
            data['rhb'] = 0
        else:
            data['rhb'] = hits / innings_pitched
        data['lhb'] = 1
        return data
    else:
        raise ValueError("argument 'type' must either be 'hitter' or 'pitcher'")

def extractData(teams):
    """
    extracts necessary data from website to instantiate Player objects
    :param teams: list of Team objects
    :return: lists of Hitter & Pitcher objects
    """
    hitters, pitchers = [], []
    for team in teams:
        print(team.name)
        print("-"*20)
        for member in team.batting:
            print(member.name)
            # extract necessary data
            page = requests.get(URL + member.endpoint)
            soup = BeautifulSoup(page.content, 'html.parser')
            # search for table
            table = searchForTable(soup, "batting_standard")
            data = extractFromTable(table, "hitter")
            # instantiate hitter & add to list
            hitter = Player.Hitter(member.name,data['rhp'],data['lhp'],
                                   data['pow'],data['avg'],data['fin'],
                                   data['gro'],data['fly'],data['hme'],data['awy'])
            hitters.append(hitter)
        for member in team.pitching:
            print(member.name)
            page = requests.get(URL + member.endpoint)
            soup = BeautifulSoup(page.content, 'html.parser')
            # search for table
            table = searchForTable(soup, "pitching_standard")
            # extract data
            data = extractFromTable(table, "pitcher")
            # instantiate pitcher & add to list
            pitcher = Player.Pitcher(member.name, data['rhb'], data['lhb'])
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
