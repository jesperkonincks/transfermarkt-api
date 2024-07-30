from dataclasses import dataclass
from datetime import datetime

from app.services.base import TransfermarktBase
from app.utils.regex import REGEX_DOB
from app.utils.utils import clean_response, extract_from_url, safe_regex
from app.utils.xpath import Agencies

@dataclass
class TransfermarktAgencyPlayers(TransfermarktBase):
    agency_id: str = None
    URL: str = "https://www.transfermarkt.com/-/beraterfirma/berater/{agency_id}/plus/1"

    def __post_init__(self) -> None:
        self.URL = self.URL.format(agency_id=self.agency_id)
        self.page = self.request_url_page()
        self.raise_exception_if_not_found(xpath=Agencies.Players.CLUB_NAME)
        self.__update_past_flag()

    def __update_past_flag(self) -> None:
        self.past = "Current club" in self.get_list_by_xpath(Agencies.Players.PAST_FLAG)

    def __parse_agency_players(self) -> list[dict]:
        page_nationalities = self.page.xpath(Agencies.Players.PAGE_NATIONALITIES)
        page_players_infos = self.page.xpath(Agencies.Players.PAGE_INFOS)

        players_ids = [extract_from_url(url) for url in self.get_list_by_xpath(Agencies.Players.URLS)]
        players_names = self.get_list_by_xpath(Agencies.Players.NAMES)
        players_ages = [
            safe_regex(dob_age, REGEX_DOB, "age") for dob_age in self.get_list_by_xpath(Agencies.Players.DOB_AGE)
        ]
        players_nationalities = [nationality.xpath(Agencies.Players.NATIONALITIES) for nationality in page_nationalities]
        players_current_club = (
            self.get_list_by_xpath(Agencies.Players.Past.CURRENT_CLUB) if self.past else [None] * len(players_ids)
        )
        players_contracts = (
            [None] * len(players_ids) if self.past else self.get_list_by_xpath(Agencies.Players.Past.CONTRACTS)
        )
        players_marketvalues = self.get_list_by_xpath(Agencies.Players.MARKET_VALUES)

        return [
            {
                "id": idx,
                "name": name,
                "age": age,
                "nationality": nationality,
                "currentClub": current_club,
                "contract": contract,
                "marketValue": market_value
            }
            for idx, name, age, nationality, current_club, contract, market_value in zip(
                players_ids,
                players_names,
                players_ages,
                players_nationalities,
                players_current_club,
                players_contracts,
                players_marketvalues
            )
        ]
    
    def get_agency_players(self) -> dict:
        self.response["id"] = self.agency_id
        self.response["players"] = self.__parse_agency_players()
        self.response["updatedAt"] = datetime.now()

        return clean_response(self.response)