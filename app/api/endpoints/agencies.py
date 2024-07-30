from typing import Optional

from fastapi import APIRouter

from app.services.agencies.players import TransfermarktAgencyPlayers

router = APIRouter()

# @router.get("/search/{agency_name}")
# def search_agencies(agency_name: str, page_number: Optional[int] = 1) -> dict:
#     tfmkt = TransfermarktAgencySearch(query=agency_name, page_number=page_number)
#     found_agencies = tfmkt.search_agency()
#     return found_agencies

# @router.get("/{agency_id}/profile")
# def get_agency_profile(agency_id: str) -> dict:
#     tfmkt = TransfermarktAgencyProfile(agency_id=agency_id)
#     agency_profile = tfmkt.get_agency_profile()
#     return agency_profile

@router.get("/{agency_id}/players")
def get_agency_players(agency_id: str) -> dict:
    tfmkt = TransfermarktAgencyPlayers(agency_id=agency_id)
    agency_players = tfmkt.get_agency_players()
    return agency_players