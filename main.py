from fastapi import FastAPI
from routes import users,flights

app = FastAPI()

app.include_router(users.router)
app.include_router(flights.router)