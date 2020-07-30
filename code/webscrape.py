import requests
from bs4 import BeautifulSoup
from bs4 import Comment

URL = 'https://www.baseball-reference.com'
CURRENT_YEAR = 2020
START_YEAR = 2019

def extractGamesFromSeason(year):
    """
    extracts all game boxscore endpoints from a given year
    :param year: year to extract all game endpoints from
    :return: list of game boxscore endpoints
    """
    endpoint_schedule = "/leagues/MLB/" + str(year) + "-schedule.shtml"
    page = requests.get(URL + endpoint_schedule)
    soup = BeautifulSoup(page.content, 'html.parser')

    endpoints = soup.find_all(string="Boxscore")
    for i in range(len(endpoints)):
        endpoints[i] = endpoints[i].parent['href']

    return endpoints

def extractTeams(endpoint_game):
    """
    extracts away & home team names
    :param endpoint_game: endpoint to game
    :return: away & home team names
    """
    page = requests.get(URL + endpoint_game)
    soup = BeautifulSoup(page.content, 'html.parser')

    scorebox = soup.find(class_="scorebox")
    strong = scorebox.find_all(attrs={"itemprop": "name"})
    team_away = strong[0].string
    team_home = strong[1].string

    return team_away, team_home

def extractTeamID(team):
    """
    gets the team id format from the team name
    :param team: string of team name
    :return: string of team in id format
    """
    id = ""
    for char in team:
        if char.isalpha():
            id += char
    return id

def searchForTable(soup, id):
    """
    searches for the table given the id of the table even if it is commented out
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

def extractPlayerEndpointsFromTable(table):
    """
    extracts endpoints of each player from given table
    :param table: table Tag object
    :return: list of player endpoints
    """
    endpoints = []
    tbody = table.find("tbody")
    trs = tbody.find_all("tr")
    for tr in trs:
        th = tr.select("th[data-stat='player']")[0]
        a = th.find("a")
        endpoints.append(a['href'])
    return endpoints

def extractHitterOutcome(endpoint_player):
    """
    extracts the player's stats for the game (only deals with hitters)
    for the Ground Truth of the model
    :param endpoint_player: endpoint of player
    :return: the player's hits / team's total hits
    """

def extractPlayerCareerStats(endpoint_player, players_all, type, year):
    """
    extracts the player's stats for his entire career (up until the game)
    for input to the model
    :param endpoint_player: endpoint to player profile
    :param players_all: list of Player objects to update if needed
    :param type: 'hitter' or 'pitcher'
    :param year: current year of season
    :return: returns updated list of Player objects
    """
    # invalid argument
    if type != 'hitter' and type != 'pitcher':
        raise ValueError("argument 'type' must either be 'hitter' or 'pitcher'")
    # hitter
    elif type == 'hitter':
        pass
    # pitcher
    else:
        pass
