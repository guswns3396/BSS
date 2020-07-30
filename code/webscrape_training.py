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

    endpoints = []
    endpoints = soup.find_all(string="Boxscore")
    for i in range(len(endpoints)):
        endpoints[i] = endpoints[i].parent['href']

    return endpoints