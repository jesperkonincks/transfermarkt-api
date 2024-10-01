from dataclasses import dataclass
from datetime import datetime

from app.services.base import TransfermarktBase
from app.utils.utils import extract_from_url
from app.utils.xpath import Tournaments

@dataclass
class TransfermarktTournamentClubs(TransfermarktBase):
    tournament_id: str = None
    URL: str = "https://www.transfermarkt.com/-/gesamtspielplan/pokalwettbewerb/{tournament_id}"

    def __post_init__(self) -> None:
        """Initialize the TransfermarkttournamentClubs class."""
        self.URL = self.URL.format(tournament_id=self.tournament_id)
        self.page = self.request_url_page()
        # self.raise_exception_if_not_found(xpath=Tournaments.Profile.NAME)

    def __parse_tournament_clubs(self) -> list:
        """
        Parse the tournament's page and extract information about the football clubs participating
            in the tournament.

        Returns:
            list: A list of dictionaries, where each dictionary contains information about a
                football club in the tournament, including the club's unique identifier and name.
        """
        urls = self.get_list_by_xpath(Tournaments.Clubs.URLS)
        names = self.get_list_by_xpath(Tournaments.Clubs.NAMES)
        ids = [extract_from_url(url) for url in urls]

        return [{"id": idx, "name": name} for idx, name in zip(ids, names)]
    

    def get_tournament_clubs(self) -> dict:
        """
        Retrieve and parse the list of football clubs participating in a specific tournament.

        Returns:
            dict: A dictionary containing the tournament's unique identifier, name, season identifier, list of clubs
                  participating in the tournament, and the timestamp of when the data was last updated.
        """
        self.response["id"] = self.tournament_id
        self.response["name"] = self.URL
        self.response["clubs"] = self.__parse_tournament_clubs()
        self.response["updatedAt"] = datetime.now()

        return self.response
