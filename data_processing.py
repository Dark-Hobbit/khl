import logging

import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
logger = logging.getLogger(__name__)


class Match:
    def __init__(self, season_id: int, match_id: int) -> None:
        self.season_id = season_id
        self.match_id = match_id
    
    
    def get_match_protocol(self) -> None:
        url = f'https://en.khl.ru/game/{self.season_id}/{self.match_id}/protocol/'
        response = requests.get(url)
        if response.status_code == 200:
            logger.info(f'Found match {self.match_id} of season {self.season_id}')
            self.protocol = response.text
            self.parsed = False
        else:
            logger.error(response)
        