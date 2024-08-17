
from dataclasses import dataclass
from datetime import datetime
from app.services.base import TransfermarktBase
from app.utils.utils import clean_response, extract_from_url
from app.utils.xpath import Clubs


@dataclass
class TransfermarktClubBreakThrough(TransfermarktBase):
    """
    A  class for retrieving and parsing the break through players of a football club from Transfermarkt.

    Args:
        club_id (str): The unique identifier of the football club.
        URL (str): The URL template for the club's players page on Transfermarkt.
    """

    club_id: str = None
    URL: str = "https://www.transfermarkt.nl/-/jugendarbeit/verein/{club_id}/wettbewerb_id/NL1/option/0/art/0/plus/1"

    def __post_init__(self) -> None:
        """Initialize the TransfermarktClubBreakThrough class."""
        self.URL = self.URL.format(club_id=self.club_id)
        self.page = self.request_url_page()
        # self.raise_exception_if_not_found(xpath=Clubs.BreakThrough)
    
    def __parse_club_break_trough_players(self) -> list[dict]:
        """
        Parse player information from the webpage and return a list of dictionaries, each representing a player.

        Returns:
            list[dict]: A list of player information dictionaries.
        """

        players_ids = [extract_from_url(url) for url in self.get_list_by_xpath(Clubs.BreakThrough.URLS)]
        players_names = self.get_list_by_xpath(Clubs.BreakThrough.NAMES)
        page_nationalities = self.page.xpath(Clubs.BreakThrough.PAGE_NATIONALITIES)
        page_clubs = self.page.xpath(Clubs.BreakThrough.PAGE_CLUBS)

        players_nationalities = [
            nationality.xpath(Clubs.BreakThrough.NATIONALITIES)
            for nationality in page_nationalities
        ]
        players_clubs = [club.xpath(Clubs.BreakThrough.CLUBS) for club in page_clubs]

        return [
            {
                "id": player_id,
                "name": name,
            }
            for player_id, name in zip(
                players_ids, players_names
            )
        ]
    
    def get_club_break_through_players(self) -> dict:
        """
        Retrieve and parse player information for the specified football club.

        Returns:
            dict: A dictionary containing the club's unique identifier, player information and the timestamp of when
                    the data was last updated.
        """
        self.response["id"] = self.club_id
        self.response["players"] = self.__parse_club_break_trough_players()
        self.response["updatedAt"] = datetime.now()

        return clean_response(self.response)