from dataclasses import dataclass
from datetime import datetime
from typing import List

from app.services.base import TransfermarktBase
from app.utils.regex import REGEX_DOB
from app.utils.utils import clean_response, extract_from_url, safe_regex
from app.utils.xpath import Agencies

@dataclass
class TransfermarktAgencyPlayers(TransfermarktBase):
    """
    A class for retrieving and parsing the players of an agency from Transfermarkt.

    Args:
        agency_id (str): The unique identifier of the agency.
        URL (str): The URL template for the agency page on Transfermarkt.
    """
    agency_id: str = None
    URL: str = "https://transfermarkt.com/-/beraterfirma/berater/{agency_id}/plus/1"
    
    def __post_init__(self) -> None:
        """Initialize the TransfermarktAgencyPlayer class."""
        self.URL = self.URL.format(agency_id=self.agency_id)
        self.page = self.request_url_page()
        # self.raise_exception_if_not_found(xpath=Agencies.Players.CLUB_NAME)

    def __get_max_page(self) -> int:
        """Get the maximum number of pages."""
        pagination = self.page.xpath("//ul[contains(@class, 'tm-pagination')]//li[contains(@class, 'tm-pagination__list-item')]//a/@title")
        max_page = 1
        for item in pagination:
            if item.startswith("Go to the last page"):
                max_page = int(item.split()[-1].strip(')'))
                break
        return max_page

    def __get_page_url(self, page_number: int) -> str:
        """Get the URL for a specific page number."""
        return f"{self.URL}/page/{page_number}"

    def __parse_agency_players_page(self, page) -> List[str]:
        """Parse players from a single page."""
        return [extract_from_url(url) for url in page.xpath(Agencies.Players.URLS)]

    def __parse_agency_players(self) -> List[str]:
        """Parse all players from all pages."""
        max_page = self.__get_max_page()
        all_players = []

        for page_num in range(1, max_page + 1):
            if page_num == 1:
                page = self.page
            else:
                page_url = self.__get_page_url(page_num)
                page = self.request_url_page(page_url)
            
            players = self.__parse_agency_players_page(page)
            all_players.extend(players)

        return all_players
    
    def get_agency_players(self) -> dict:
        self.response["id"] = self.agency_id
        self.response["players"] = self.__parse_agency_players()
        self.response["updatedAt"] = datetime.now()

        return clean_response(self.response)