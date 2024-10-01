from dataclasses import dataclass
from datetime import datetime

from app.services.base import TransfermarktBase
from app.utils.utils import extract_from_url
from app.utils.xpath import Competitions

@dataclass
class TransfermarktCountrySearch(TransfermarktBase):
    country_id: str = None
    URL: str = "https://www.transfermarkt.com/-/national/wettbewerbe/{country_id}/saison_id/{season_id}/plus/1"

    def __post_init__(self) -> None:
        self.URL = self.URL.format(country_id=self.country_id, season_id=self.season_id)
        self.page = self.request_url_page()
    
    def __parse_search_results(self) -> list:
        idx = [extract_from_url(url) for url in self.get_list_by_xpath(Competitions.Country.URLS)]
        name = self.get_list_by_xpath(Competitions.Country.NAMES)

        return [
            {
                "id": idx,
                "name": name
            }
            for idx, name in zip(
                idx, name
            )
        ]
    
    def get_country(self) -> dict:
        self.response["country_id"] = self.country_id
        self.response["season_id"] = self.season_id
        self.response["results"] = self.__parse_search_results()
        self.response["updatedAt"] = datetime.now()

        return self.response