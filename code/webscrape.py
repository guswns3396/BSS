import requests
import code.Player as Player
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

def extractTeams(soup):
    """
    extracts away & home team names
    :param soup: Soup object of game
    :return: away & home team names
    """
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

def extractHitterOutcome(table, endpoint_player):
    """
    extracts the player's stats for the game (only deals with hitters)
    for the Ground Truth of the model
    :param: table: table Tag object of the game batting results
    :param endpoint_player: endpoint of player
    :return: the player's hits / team's total hits (h_contribution)
    """
    # find player's hits
    a = table.find(attrs={'href': endpoint_player})
    tr = a.find_parent("tr")
    h = int(tr.find(attrs={"data-stat":"H"}).string)

    # find team's total hits
    th = table.find(string="Team Totals").parent
    h_total = int(th.find_next_sibling(attrs={"data-stat":"H"}).string)
    
    # calculate contribution
    h_contribution = h / h_total
    return h_contribution

def extractPlayerName(div):
    """
    parses player's name
    :param div: div Tag object of player's overview
    :return: name of player
    """
    selector = " h1[itemprop='name']"
    h1 = div.select(selector)[0]
    name = h1.find("span").string
    return name

def extractPlayerHand(div, type):
    """
    parses player's dominant hand depending on type
    r => right, l => left
    1 => uses that hand, 0 => does not use that hand
    :param div: div Tag object of player's overview
    :param type: 'hitter' or 'pitcher'
    :return: r & l
    """
    if type != 'hitter' and type != 'pitcher':
        raise ValueError("argument 'type' must either be 'hitter' or 'pitcher'")

    r = 0
    l = 0
    hand = div.find('p').find_next_sibling('p').contents
    if type == 'hitter':
        hand = hand[2]
        if 'left' in hand.lower():
            l = 1
        if 'right' in hand.lower():
            r = 1
    else:
        hand = hand[4]
        if 'left' in hand.lower():
            l = 1
        if 'right' in hand.lower():
            r = 1
    return r, l

def checkPlayersLastSeasonStats(endpoint_player, type, year_current):
    """
    checks if the player's last year stats exists
    returns last year's stats if exists
    returns 0 if not
    :param endpoint_player: endpoint to player
    :param type: 'hitter' or 'pitcher'
    :param year_current: current year
    :return: Player object corresponding to type with stats
    """
    if type != 'hitter' and type != 'pitcher':
        raise ValueError("argument 'type' must either be 'hitter' or 'pitcher'")

    page = requests.get(URL + endpoint_player)
    soup = BeautifulSoup(page.content, 'html.parser')

    selector = "#meta div[itemtype='https://schema.org/Person']"
    div = soup.select(selector)[0]

    name = extractPlayerName(div)
    # extract other data
    if type == 'hitter':
        r, l = extractPlayerHand(div, type)
        table = searchForTable(soup, 'batting_standard')
        # default if table X exist
        if table == None:
            return Player.Hitter(name,endpoint_player,0,0,0,r,l)
        # parse table
        else:
            pass
    else:
        r, l = extractPlayerHand(div, type)
        table = searchForTable(soup, "pitching_standard")

def extractPlayerCareerStats(endpoint_player, players_stats, type, year):
    """
    extracts the player's stats for his entire career (up until the game)
    for input to the model
    :param endpoint_player: endpoint to player profile
    :param players_stats: dict of Player objects to update if needed
    :param type: 'hitter' or 'pitcher'
    :param year: current year of season
    :return: returns updated dict of Player objects
    """
    # invalid argument
    if type != 'hitter' and type != 'pitcher':
        raise ValueError("argument 'type' must either be 'hitter' or 'pitcher'")

    # hitter
    elif type == 'hitter':
        # see if hitter in dict (not the first game of season)
        if endpoint_player in players_stats:
            pass
        # if not in dict use last year's stats (first game of season)
        else:
            pass

    # pitcher
    else:
        pass

def extractTrainingSet():
    # go through all the seasons from start year to current year
    # including current year
    for i in range(START_YEAR,CURRENT_YEAR + 1):
        endpoints_game = extractGamesFromSeason(i)
        hitters_stats = {}
        pitchers_stats = {}

        # go through all games in the given year
        for endpoint_game in endpoints_game:
            page = requests.get(URL + endpoint_game)
            soup = BeautifulSoup(page.content, 'html.parser')
            team_away, team_home = extractTeams(soup)

            ## Training Example for Away Team ##
            hitters = []
            pitchers = []
            # look at batting results of away team
            table = searchForTable(soup, extractTeamID(team_away) + 'batting')
            # look at pitching results of home team
            table = searchForTable(soup, extractTeamID(team_home) + 'pitching')

            ## Training Example for Home Team ##
            # look at batting results of home team
            # look at pitching results of away team