from dataclasses import dataclass
from datetime import datetime

from app.services.base import TransfermarktBase
from app.utils.utils import extract_from_url
from app.utils.xpath import Agencies

@dataclass
class TransfermarktAgencySearch(TransfermarktBase):
    """
    A class for searching football agencies on Transfermarkt and retrieving search results.

    Args:
        query (str): The search query for finding football agencies
        URL (str): The URL template for the search query.
        page_number (int): Th epage number of search results (default is 1)
    """

    query: str = None
    URL: str = (
        "https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche?query={query}&Verein_page={page_number}"
    )
    page_number: int = 1

    def __post_init__(self) -> None:
        """Initialize the TransfermarktAgencySearch class."""
        self.URL = self.URL.format(query=self.query, page_number=self.page_number)
        self.page = self.request_url_page

    def __parse_search_results(self) -> list:
        """
        Parse the search results page and extract information about the found agencies.

        Returns:
            list: A list of dictionaries, where each dictionary contains information about 
                an agency found in teh search results.
        """

        agencies_names = self.get_list_by_xpath(Agencies.Search.NAMES)
        agencies_urls = self.get_list_by_xpath(Agencies.Search.URLS)

        agencies_ids = [extract_from_url(url) for url in agencies_urls]

        return [
            {
                "id": idx,
                "url": url,
            }
            for idx, url in zip(
                agencies_ids,
                agencies_urls,
                agencies_names
            )
        ]
    
    def search_agencies(self) -> dict:
        """
        Perform a search for football agencies on Transfermarkt.

        Returns:
            dict: A dictionary containing the search results, current page number, last page number,
                search results, and the timestamp of when the search was conducted.
        """
        self.response["query"] = self.query
        self.response["pageNumber"] = self.page_number,
        self.response["lastPageNumber"] = self.get_last_page_number(Agencies.Search.BASE)
        self.response["results"] = self.__parse_search_results()
        self.response["updatedAt"] = datetime.now()

        return self.response