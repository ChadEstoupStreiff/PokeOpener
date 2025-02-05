import logging
import random

from fastapi import APIRouter, Depends
from logic.db import get_db
from logic.models import Item, User
from pokemontcgsdk import Card
from sqlalchemy.orm import Session
from views.auth import get_current_user

router = APIRouter(prefix="/cards", tags=["Authentification"])


logging.info("Loading all cards id")
with open("cards_id.txt", "r") as f:
    cards_id = f.readlines()
logging.info(f"Loaded {len(cards_id)} cards id")


@router.get("/draw")
def draw_card(token: str, db: Session = Depends(get_db)):
    user = User.get_user_by_id(db, get_current_user(token))

    card = Card.find(cards_id[random.randint(0, len(cards_id) - 1)])
    Item.add_card(db, user.id, card.id)
    db.close()

    return card


@router.get("/get")
def get_card(card_id: str):
    card = Card.find(card_id)
    return card


@router.get("/inventory")
def get_inventory(token: str, db: Session = Depends(get_db)):
    user = User.get_user_by_id(db, get_current_user(token))
    items = Item.get_card_of_user(db, user.id)
    db.close()
    return items
