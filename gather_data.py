import logging
import requests
import bs4
from classes import Match, Player

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
logger = logging.getLogger(__name__)

        
def get_match(season_id: str, match_id: str) -> Match:
    protocol = get_protocol(season_id, match_id)
    match_data = parse_protocol(protocol, season_id, match_id)
    match = Match(season_id, match_id)
    match.update_match_data(**match_data)
    return match

def get_protocol(season_id: str, match_id: str) -> str:
    url = f'https://en.khl.ru/game/{season_id}/{match_id}/protocol/'
    response = requests.get(url)
    if response.status_code == 200:
        logger.info(f'Found match {match_id} of season {season_id}')
        return response.text
    else:
        logger.error(response)
    
def parse_protocol(protocol: str, season_id: str, match_id: str) -> dict:
    main = bs4.BeautifulSoup(protocol, 'html.parser').find('main')
    match_data = {}
    match_data['date'] = main.h2.text.split('/')[1].strip()
    
    home_team, away_team = main.find_all('div', class_='preview-frame__club')
    home_name, home_coach = get_team_data(home_team)
    away_name, away_coach = get_team_data(away_team)
    match_data.update(home_team = home_name, home_team_coach = home_coach,
                     away_team = away_name, away_team_coach = away_coach)

    score = main.find('div', 'preview-frame__center')
    score_string, winner, length = get_score(score)
    match_data.update(score = score_string, winner = match_data[winner], length = length)
    
    home_tables = main.find_all(class_='wrapper-content mr-30__1280')[:3]
    home_players = parse_team_players(home_tables, home_name, season_id, match_id)
    away_tables = main.find_all(class_='wrapper-content mr-30__1280')[3:6]
    away_players = parse_team_players(away_tables, home_name, season_id, match_id)
    match_data.update(home_team_players = home_players, away_team_players = away_players)
    return match_data

def get_team_data(team: bs4.element.Tag) -> tuple[str, str]:
    name = team.a.text.strip()
    coach = team.find('p', class_='preview-frame__club-nameTrainer').text.strip()
    return name, coach

def get_score(score: bs4.element.Tag) -> tuple[str, str, str]:
    score = score.p.text.split()
    if len(score) < 2 or not score[0].isnumeric() or not score[1].isnumeric():
        return
    score_string = f'{score[0]} - {score[1]}'
    winner = 'undecided'
    if score[0] > score[1]:
        winner = 'home_team'
    elif score[0] < score[1]:
        winner = 'away_team'
    else:
        logger.error(f'Match is a draw?')
    
    length = 'undecided'
    if len(score) == 2:
        length = 'normal'
    elif score[2] == 'OT':
        length = 'overtime'
        score_string += ' OT'
    elif score[2] == 'SO':
        length = 'shootouts'
        score_string += ' SO'
    else:
        logger.error(f'Match has weird length')
    return score_string, winner, length 

def parse_table_header(table_header: bs4.element.Tag) -> list[str, ...]:
    header = []
    for column in table_header.find_all('th'):
        if column.title:
            header.append(column.title.strip())
        elif column.text.strip() != 'Player':
            header.append(column.text.strip())
    return header

def parse_player_stats(player_stats: bs4.element.Tag) -> tuple[str, str, dict]:
    stats = []
    for column in player_stats.find_all('th'):
        if column.a:
            player_id = column.a['href'].split('/')[-2]
            name = column.a.text.strip()
        else:
            stats.append(column.text.strip())
    return player_id, name, stats

def parse_player_table(player_table: bs4.element.Tag, team_name: str, season_id: str, match_id: str) -> list[Player, ...]:
    position = player_table.h3.text.strip().rstrip('s')
    header = parse_table_header(player_table.thead)
    players = []
    for line in player_table.tbody.find_all('tr'):
        player_id, name, values = parse_player_stats(line)
        stats = dict(zip(header, values))
        stats['Team'] = team_name
        player = Player(player_id, name, position)
        player.add_match_record(season_id, match_id, stats)
        players.append(player)
    return players

def parse_team_players(player_tables: list[bs4.element.Tag], team_name: str, season_id: str, match_id: str) -> list[Player, ...]:
    team_players = []
    for table in player_tables:
        players = parse_player_table(table, team_name, season_id, match_id)
        team_players.extend(players)
    return team_players
