from pydantic import BaseModel
from typing import Optional, Union, List
from datetime import date
from queries.pool import pool

# Example of more complicated modeling
# class Thought(BaseModel):
#   private_thoughts: str
#   public_thoughts: str

class Error(BaseModel):
  message: str

class VacationIn(BaseModel):
  name: str
  from_date: date
  to_date: date
  thoughts: Optional[str]

class VacationOut(BaseModel):
  id: int
  name: str
  from_date: date
  to_date: date
  thoughts: Optional[str]

class VacationRepository:
  def get_all(self) -> Union[Error, List[VacationOut]]:
    try:
      with pool.connection() as conn:
        # get a cursor
        with conn.cursor() as db:
          # Run our SELECT statement
          result = db.execute(
            """
            SELECT id, name, from_date, to_date, thoughts
            FROM vacations
            ORDER BY from_date;
            """
          )

          return [
            VacationOut(
              id=record[0],
              name=record[1],
              from_date=record[2],
              to_date=record[3],
              thoughts=record[4]
            )
            for record in db
          ]
    except Exception as e:
      print(e)
      return { "message": "Could not retrieve vacations" }

  def create(self, vacation: VacationIn) -> VacationOut:
    # connect the database
    with pool.connection() as conn:
      # get a cursor
      with conn.cursor() as db:
        # Run our insert statement
        result = db.execute(
          """
            INSERT INTO vacations
              (name, from_date, to_date, thoughts)
            VALUES
              (%s, %s, %s, %s)
            RETURNING id;
          """,
          [
            vacation.name,
            vacation.from_date,
            vacation.to_date,
            vacation.thoughts
          ]
        )
        # Return new data
        id = result.fetchone()[0]
        old_data = vacation.dict()

        return VacationOut(id=id, **old_data)
