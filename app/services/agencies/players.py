from dataclasses import dataclass
from datetime import datetime

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

    def __parse_agency_players(self) -> list[dict]:
        players_ids = [extract_from_url(url) for url in self.get_list_by_xpath(Agencies.Players.URLS)]

        return players_ids
    
    def get_agency_players(self) -> dict:
        self.response["id"] = self.agency_id
        self.response["players"] = self.__parse_agency_players()
        self.response["updatedAt"] = datetime.now()

        return clean_response(self.response)