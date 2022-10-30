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
