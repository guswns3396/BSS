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
