from fastapi import FastAPI
from routers import vacations


app = FastAPI()
app.include_router(vacations.router)
