import logging
import copy

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
logger = logging.getLogger(__name__)


class Match:
    
    def __init__(self, season_id: int, match_id: int) -> None:
        self.season_id = season_id
        self.match_id = match_id
    
    def __repr__(self):
        try:
            return f'{self.date}: {self.home_team} - {self.away_team}'
        except:
            return f'Missing data: season {self.season_id}, match {self.match_id}'
    
    
    def update_match_data(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)
    
    @property
    def dict_(self) -> dict:
        result = copy.deepcopy(vars(self))
        if 'home_team_players' in result:
            for i, player in enumerate(result['home_team_players']):
                result['home_team_players'][i] = player.dict_
        if 'away_team_players' in result:
            for i, player in enumerate(result['away_team_players']):
                result['away_team_players'][i] = player.dict_
        return result
        
class Player:
    
    def __init__(self, player_id: int, name: str, position: str) -> None:
        self.id = player_id
        self.name = name
        self.position = position
        self.stats = {}
        
    def __repr__(self):
        return f'{self.position} - {self.name}'
    
    
    def add_match_record(self, season_id: int, match_id: int, match_stats: dict[str, int]) -> None:
        if season_id not in self.stats:
            self.stats[season_id] = {}
        self.stats[season_id][match_id] = match_stats
    
    @property
    def dict_(self) -> dict:
        result = copy.deepcopy(vars(self))
        return result