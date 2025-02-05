import logging

from dotenv import dotenv_values
from fastapi import FastAPI
from logic.db import DB
from logic.models import Base
from pokemontcgsdk import RestClient

config = dotenv_values("/.env")
logging.info("Config: %s", config)
RestClient.configure(config["POKE_API_KEY"])

logging.info("Init db")
Base.metadata.create_all(bind=DB().engine)

logging.info("Init FastAPI")
app = FastAPI()


import views.auth

app.include_router(views.auth.router)

import views.cards

app.include_router(views.cards.router)