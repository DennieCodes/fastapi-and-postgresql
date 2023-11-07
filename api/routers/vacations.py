from fastapi import APIRouter, Depends, Response
from typing import Union, List
from queries.vacations import (
  Error,
  VacationIn,
  VacationRepository,
  VacationOut
)

router = APIRouter()

@router.post("/vacations", response_model=Union[VacationOut, Error])
def create_vacations(
  vacation: VacationIn,
  response: Response,
  repo: VacationRepository = Depends()
):
  response.status_code = 400
  return repo.create(vacation)

@router.get("/vacations", response_model=Union[VacationOut, Error])
def get_all(
  repo: VacationRepository = Depends()
):
  return repo.get_all()