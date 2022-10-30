import logging

import requests
import bs4

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
logger = logging.getLogger(__name__)


class Match:
    
    def __init__(self, season_id: int, match_id: int, parsed: bool = False) -> None:
        self.season_id = season_id
        self.match_id = match_id
        self.parsed = parsed
    
    
    def get_match_protocol(self) -> None:
        url = f'https://en.khl.ru/game/{self.season_id}/{self.match_id}/protocol/'
        response = requests.get(url)
        if response.status_code == 200:
            logger.info(f'Found match {self.match_id} of season {self.season_id}')
            return response.text
        else:
            logger.error(response)
    
    def get_match_summary(self, protocol: str) -> None:
        
        def parse_team(team: bs4.element.Tag) -> tuple[str, str]:
            name = team.a.text.strip()
            coach = team.find('p', class_='preview-frame__club-nameTrainer').text.strip()
            return name, coach
        
        def parse_score(score: bs4.element.Tag) -> tuple[str, str]:
            score = score.p.text.split()
            logger.debug(f'{self.match_id}-{self.season_id} score is {score}')
            winner = 'undecided'
            length = 'undecided'
            
            if score[0] > score[1]:
                winner = 'home_team'
            elif score[0] < score[1]:
                winner = 'away_team'
            else:
                logger.error(f'Match {self.match_id} of season {self.season_id} is a draw')

            if len(score) == 2:
                length = 'normal'
            elif score[2] == 'OT':
                length = 'overtime'
            elif score[2] == 'SO':
                length = 'shootouts'
            else:
                logger.error(f'Match {self.match_id} of season {self.season_id} has weird length')

            return winner, length 
            
        main = bs4.BeautifulSoup(protocol, 'html.parser').find('main')
        self.date = main.h2.text.split('/')[1].strip()
        
        home_team = main.find('div', class_='preview-frame__club_left')
        self.home_team, self.home_team_coach = parse_team(home_team)
        away_team = main.find('div', class_='preview-frame__club_right')
        self.away_team, self.away_team_coach = parse_team(away_team)
        
        score = main.find('div', 'preview-frame__center')
        self.winner, self.length = parse_score(score)
        self.winner = getattr(self, self.winner)
    
    def get_player_summary(self, protocol: str) -> None:

        def parse_table_header(table_header: bs4.element.Tag) -> list[str, ...]:
            header = []
            for line in table_header.find_all('th'):
                if line.title:
                    header.append(line.title.strip())
                elif line.text.strip() != 'Player':
                    header.append(line.text.strip())
            return header
        
        def parse_player_stats(player_stats: bs4.element.Tag) -> tuple[str, str, dict[str, int]]:
            stats = []
            for value in player_stats.find_all('th'):
                if value.a:
                    player_id = value.a['href'].split('/')[-2]
                    name = value.a.text.strip()
                else:
                    stats.append(value.text.strip())
            return player_id, name, stats
        
        def parse_player_table(player_table: bs4.element.Tag, team_name: str) -> list[Player, ...]:
            position = player_table.h3.text.strip().rstrip('s')
            header = parse_table_header(player_table.thead)
            players = []
            for line in player_table.tbody.find_all('tr'):
                player_id, name, values = parse_player_stats(line)
                
                stats = dict(zip(header, values))
                stats['Team'] = team_name
                player = Player(player_id, name, position)
                player.add_match_record(self.season_id, self.match_id, stats)
                players.append(player)
            return players
        
        def parse_team_players(player_tables: list[bs4.element.Tag], team_name: str) -> list[Player, ...]:
            team_players = []
            for table in player_tables:
                players = parse_player_table(table, team_name)
                team_players.extend(players)
            return team_players
        
        main = bs4.BeautifulSoup(protocol, 'html.parser').find('main')
        home_team_players = main.find_all(class_='wrapper-content mr-30__1280')[:3]
        self.home_team_players = parse_team_players(home_team_players, self.home_team)
        away_team_players = main.find_all(class_='wrapper-content mr-30__1280')[3:6]
        self.away_team_players = parse_team_players(away_team_players, self.away_team)
        
        self.parsed = True
        
        
class Player:
    
    def __init__(self, player_id: int, name: str, position: str) -> None:
        self.id = player_id
        self.name = name
        self.position = position
        self.records = {}
    
    
    def add_match_record(self, season_id: int, match_id: int, match_stats: dict[str, int]) -> None:
        if season_id not in self.records:
            self.records[season_id] = {}
        self.records[season_id][match_id] = match_stats
