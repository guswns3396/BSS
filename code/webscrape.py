import requests
import copy
from code.Player import Hitter, Pitcher
from code.Game import Game
from bs4 import BeautifulSoup
from bs4 import Comment

URL = 'https://www.baseball-reference.com'
YEAR_CURRENT = 2020
YEAR_START = 2019

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
    if table is None:
        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        id_str = "id=\"" + id + "\""

        for comment in comments:
            if id_str in comment:
                table = comment
                table = table[len("<!--"):-len("-->")].strip()
                table = BeautifulSoup(table, 'html.parser')
                table = table.find(id=id)
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

def extractSeasonStatsFromTable(table, type, year):
    """
    parses necessary data from the player's season stats table depending on the type
    if table is None, default values are used
    if given year's stats don't exist, default values are used
    :param table: table Tag object of player's stats
    :param type: 'hitter' or 'pitcher'
    :param year: year of season to extract data from
    :return: dict of player's stats required to instantiate Player class
    """
    data = {}
    if type == "hitter":
        # default values
        pa = 0
        h = 0
        so = 0
        # table found
        if table is not None:
            tr = table.find(id="batting_standard." + str(year))
            # year found
            if tr is not None:
                pa = int(tr.find(attrs={'data-stat': 'PA'}).string)
                h = int(tr.find(attrs={'data-stat': 'H'}).string)
                so = int(tr.find(attrs={'data-stat': 'SO'}).string)
        data['PA'] = pa
        data['H'] = h
        data['SO'] = so
        return data
    elif type == "pitcher":
        # default values
        sho = 0
        ip = 0
        h = 0
        so = 0
        bf = 0
        # if table found
        if table is not None:
            tr = table.find(id="pitching_standard." + str(year))
            # if year found
            if tr is not None:
                sho = int(tr.find(attrs={'data-stat': 'SHO'}).string)
                ip = float(tr.find(attrs={'data-stat': 'IP'}).string)
                h = int(tr.find(attrs={'data-stat': 'H'}).string)
                so = int(tr.find(attrs={'data-stat': 'SO'}).string)
                bf = int(tr.find(attrs={'data-stat': 'batters_faced'}).string)
        data['SHO'] = sho
        data['IP'] = ip
        data['H'] = h
        data['SO'] = so
        data['BF'] = bf
        return data
    else:
        raise ValueError("argument 'type' must either be 'hitter' or 'pitcher'")

def checkPlayersLastSeasonStats(endpoint_player, type, year):
    """
    checks if the player's last year stats exists
    uses last year's stats if exists
    uses default stats (0) if not
    then returns Player object with stats
    :param endpoint_player: endpoint to player
    :param type: 'hitter' or 'pitcher'
    :param year: year of the current season that you want the stats for
    :return: Player object corresponding to type with stats
    """
    if type != 'hitter' and type != 'pitcher':
        raise ValueError("argument 'type' must either be 'hitter' or 'pitcher'")

    page = requests.get(URL + endpoint_player)
    soup = BeautifulSoup(page.content, 'html.parser')

    selector = "#meta div[itemtype='https://schema.org/Person']"
    div = soup.select(selector)[0]

    name = extractPlayerName(div)
    r, l = extractPlayerHand(div, type)
    if type == 'hitter':
        table = searchForTable(soup, 'batting_standard')
    else:
        table = searchForTable(soup, "pitching_standard")
    data = extractSeasonStatsFromTable(table, type, year - 1)

    if type == 'hitter':
        return Hitter(name, endpoint_player, data['PA'],
                             data['H'], data['SO'], r, l)
    else:
        return Pitcher(name, endpoint_player, data['SHO'],
                              data['IP'], data['H'], data['SO'],
                              data['BF'], r, l)

def extractPlayerGamePerformance(table_results, endpoint_player, type):
    """
    extracts player's performance in a given game
    :param table_results: table Tag object of results of current game according to type
    :param endpoint_player: endpoint to player profile
    :param type: 'hitter' or 'pitcher'
    :return: dict containing player's performance in the game (stats / data)
    """
    data = {}
    a = table_results.find(attrs={'href': endpoint_player})
    tr = a.find_parent("tr")
    if type == 'hitter':
        data['PA'] = int(tr.find(attrs={'data-stat': 'PA'}).string)
        data['H'] = int(tr.find(attrs={'data-stat': 'H'}).string)
        data['SO'] = int(tr.find(attrs={'data-stat': 'SO'}).string)
    elif type == 'pitcher':
        data['IP'] = float(tr.find(attrs={'data-stat': 'IP'}).string)
        data['H'] = int(tr.find(attrs={'data-stat': 'H'}).string)
        data['SO'] = int(tr.find(attrs={'data-stat': 'SO'}).string)
        data['BF'] = int(tr.find(attrs={'data-stat': 'batters_faced'}).string)
        # determine shutout
        runs = int(tr.find(attrs={'data-stat': 'R'}).string)
        # determine if complete game
        tbody = table_results.find("tbody")
        numPitchers = len(tbody.find_all("tr"))
        if runs == 0 and numPitchers == 1:
            data['SHO'] = 1
        else:
            data['SHO'] = 0
    else:
        raise ValueError("argument 'type' must either be 'hitter' or 'pitcher'")
    return data

def extractPlayerCareerStats(endpoint_player, players_stats, type, year):
    """
    adds player to dict if not found
    returns Player object for input to model (stats up until the game)
    :param endpoint_player: endpoint to player profile
    :param players_stats: dict that maps player endpoint to Player objects
    :param type: 'hitter' or 'pitcher'
    :param year: current year of season
    :return: returns Player object
    """
    # invalid argument
    if type != 'hitter' and type != 'pitcher':
        raise ValueError("argument 'type' must either be 'hitter' or 'pitcher'")

    # see if player in dict (not the first game of season)
    if endpoint_player in players_stats:
        player = players_stats[endpoint_player]
    # if not in dict use last year's stats (first game of season)
    else:
        player = checkPlayersLastSeasonStats(endpoint_player, type, year)
        players_stats[endpoint_player] = player

    # return player's stats up until the game (pre-game)
    return player

def extractTrainingExample(endpoint_game, hitters_stats, pitchers_stats, soup, type, team_batting, team_pitching, year):
    """
    extracts Game object as training example for a given game
    :param endpoint_game: endpoint to game
    :param hitters_stats: dict of running total stats of all hitters (pre-game)
    :param pitchers_stats: dict of running total stats of all pitchers (pre-game)
    :param soup: soup object of game page
    :param type: 'away' or 'home'
    :param team_batting: name of batting team
    :param team_pitching: name of pitching team
    :param year: year of season
    :return: Game object
    """
    if type != 'away' and type != 'home':
        raise ValueError("argument 'type' must either be 'away' or 'home'")
    # list of Player objects for input
    hitters = []
    pitchers = []
    # dictionary that maps hitter endpoint to outcome (H_Contribution)
    outcome = {}
    # look at batting results
    table_results_batting = searchForTable(soup, extractTeamID(team_batting) + 'batting')
    endpoints_player = extractPlayerEndpointsFromTable(table_results_batting)
    for endpoint_player in endpoints_player:
        # get player's stats up until the game & get input for model
        hitters.append(copy.deepcopy(extractPlayerCareerStats(endpoint_player, hitters_stats, 'hitter', year)))
        # update player's status according to outcome for input to next game
        data_performance = extractPlayerGamePerformance(table_results_batting, endpoint_player, 'hitter')
        hitters_stats[endpoint_player].updateStats(data_performance)
        # ground truth
        outcome[endpoint_player] = extractHitterOutcome(table_results_batting, endpoint_player)
    # look at pitching results
    table_results_pitching = searchForTable(soup, extractTeamID(team_pitching) + 'pitching')
    endpoints_player = extractPlayerEndpointsFromTable(table_results_pitching)
    for endpoint_player in endpoints_player:
        # get player's stats up until the game & get input for model
        pitchers.append(copy.deepcopy(extractPlayerCareerStats(endpoint_player, pitchers_stats, 'pitcher', year)))
        # update player's status according to outcome for input to next game
        data_performance = extractPlayerGamePerformance(table_results_pitching, endpoint_player, 'pitcher')
        pitchers_stats[endpoint_player].updateStats(data_performance)
    # instantiate Game object for training example
    if type == 'away':
        return Game(endpoint_game + '-A', hitters, pitchers, outcome)
    else:
        return Game(endpoint_game + '-H', hitters, pitchers, outcome)

def extractTrainingSet(year_start, year_current):
    """
    extract training examples from given start year to current year
    instantiate as Game objects
    return list of Game objects (training set)
    :return: list of Game objects
    """
    games = []
    # go through all the seasons from start year to current year
    # including current year
    for year in range(year_start, year_current + 1):
        # dictionary that maps player endpoint to Player object (stats)
        # for career stats for the whole season (running tally)
        hitters_stats = {}
        pitchers_stats = {}

        endpoints_game = extractGamesFromSeason(year)
        # go through all games in the given year
        for endpoint_game in endpoints_game:
            page = requests.get(URL + endpoint_game)
            soup = BeautifulSoup(page.content, 'html.parser')
            team_away, team_home = extractTeams(soup)

            ## Training Example for Away Team ##
            games.append(extractTrainingExample(endpoint_game,hitters_stats,pitchers_stats,soup,'away',team_away,team_home))
            ## Training Example for Home Team ##
            games.append(extractTrainingExample(endpoint_game,hitters_stats,pitchers_stats,soup,'home',team_home,team_away))

    return games
