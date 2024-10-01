from typing import Optional

from fastapi import APIRouter

from app.services.competitions.clubs import TransfermarktCompetitionClubs
from app.services.competitions.country import TransfermarktCountrySearch
from app.services.competitions.search import TransfermarktCompetitionSearch
from app.services.competitions.clubsTournament import TransfermarktTournamentClubs

router = APIRouter()

@router.get("/search/country/{country_id}")
def search_competitions_country(country_id: str, season_id: Optional[int] = 2024) -> dict:
    tfmkt = TransfermarktCountrySearch(query=country_id)
    return "Not yet available"

@router.get("/search/{competition_name}")
def search_competitions(competition_name: str, page_number: Optional[int] = 1) -> dict:
    tfmkt = TransfermarktCompetitionSearch(query=competition_name, page_number=page_number)
    competitions = tfmkt.search_competitions()
    return competitions


@router.get("/{competition_id}/clubs")
def get_competition_clubs(competition_id: str, season_id: Optional[str] = None) -> dict:
    tfmkt = TransfermarktCompetitionClubs(competition_id=competition_id, season_id=season_id)
    competition_clubs = tfmkt.get_competition_clubs()
    return competition_clubs

@router.get("/{tournament_id}/clubs")
def get_tournament_clubs(tournament_id: str) -> dict:
    tfmkt = TransfermarktTournamentClubs(tournament_id=tournament_id)
    tournament_clubs = tfmkt.get_tournament_clubs()
    return tournament_clubs