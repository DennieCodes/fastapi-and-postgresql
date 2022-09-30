from pydantic import BaseModel
from typing import List, Optional, Union
from datetime import date
from queries.pool import pool


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
    def get_one(self, vacation_id: int) -> Optional[VacationOut]:
        try:
            # connect the database
            with pool.connection() as conn:
                # get a cursor (something to run SQL with)
                with conn.cursor() as db:
                    # Run our SELECT statement
                    result = db.execute(
                        """
                        SELECT id
                             , name
                             , from_date
                             , to_date
                             , thoughts
                        FROM vacations
                        WHERE id = %s
                        """,
                        [vacation_id]
                    )
                    record = result.fetchone()
                    if record is None:
                        return None
                    return self.record_to_vacation_out(record)
        except Exception as e:
            print(e)
            return {"message": "Could not get that vacation"}

    def delete(self, vacation_id: int) -> bool:
        try:
            # connect the database
            with pool.connection() as conn:
                # get a cursor (something to run SQL with)
                with conn.cursor() as db:
                    db.execute(
                        """
                        DELETE FROM vacations
                        WHERE id = %s
                        """,
                        [vacation_id]
                    )
                    return True
        except Exception as e:
            print(e)
            return False

    def update(self, vacation_id: int, vacation: VacationIn) -> Union[VacationOut, Error]:
        try:
            # connect the database
            with pool.connection() as conn:
                # get a cursor (something to run SQL with)
                with conn.cursor() as db:
                    db.execute(
                        """
                        UPDATE vacations
                        SET name = %s
                          , from_date = %s
                          , to_date = %s
                          , thoughts = %s
                        WHERE id = %s
                        """,
                        [
                            vacation.name,
                            vacation.from_date,
                            vacation.to_date,
                            vacation.thoughts,
                            vacation_id
                        ]
                    )
                    # old_data = vacation.dict()
                    # return VacationOut(id=vacation_id, **old_data)
                    return self.vacation_in_to_out(vacation_id, vacation)
        except Exception as e:
            print(e)
            return {"message": "Could not update that vacation"}

    def get_all(self) -> Union[Error, List[VacationOut]]:
        try:
            # connect the database
            with pool.connection() as conn:
                # get a cursor (something to run SQL with)
                with conn.cursor() as db:
                    # Run our SELECT statement
                    result = db.execute(
                        """
                        SELECT id, name, from_date, to_date, thoughts
                        FROM vacations
                        ORDER BY from_date;
                        """
                    )
                    # result = []
                    # for record in db:
                    #     vacation = VacationOut(
                    #         id=record[0],
                    #         name=record[1],
                    #         from_date=record[2],
                    #         to_date=record[3],
                    #         thoughts=record[4],
                    #     )
                    #     result.append(vacation)
                    # return result

                    return [
                        self.record_to_vacation_out(record)
                        for record in result
                    ]
        except Exception as e:
            print(e)
            return {"message": "Could not get all vacations"}

    def create(self, vacation: VacationIn) -> Union[VacationOut, Error]:
        try:
            # connect the database
            with pool.connection() as conn:
                # get a cursor (something to run SQL with)
                with conn.cursor() as db:
                    # Run our INSERT statement
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
                    id = result.fetchone()[0]
                    # Return new data
                    # old_data = vacation.dict()
                    # return VacationOut(id=id, **old_data)
                    return self.vacation_in_to_out(id, vacation)
        except Exception:
            return {"message": "Create did not work"}

    def vacation_in_to_out(self, id: int, vacation: VacationIn):
        old_data = vacation.dict()
        return VacationOut(id=id, **old_data)

    def record_to_vacation_out(self, record):
        return VacationOut(
            id=record[0],
            name=record[1],
            from_date=record[2],
            to_date=record[3],
            thoughts=record[4],
        )
