import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(
        String(255), primary_key=True, default=lambda: str(uuid.uuid4()), index=True
    )
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(
        String(255), nullable=True
    )  # Only for email/password users
    full_name = Column(String(255))

    def get_user_by_id(db: Session, user_id: str):
        return db.query(User).filter(User.id == user_id).first()

    def create_user(
        db: Session, email: str, hashed_password: str, full_name: str
    ):
        user = User(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
        )
        db.add(user)
        db.commit()
        return user


class Item(Base):
    __tablename__ = "items"

    id = Column(
        String(255), primary_key=True, default=lambda: str(uuid.uuid4()), index=True
    )
    owner_id = Column(String(255), ForeignKey("users.id"))
    card_id = Column(String(255))
    date_obtained = Column(DateTime)
    faved = Column(Boolean, default=False)

    def get_card_of_user(db: Session, owner_id: str):
        return db.query(Item).filter(Item.owner_id == owner_id).all()
    
    def get_specific_card_of_user(db: Session, owner_id: str, id: str):
        return db.query(Item).filter(Item.owner_id == owner_id, Item.id == id).first()

    def add_card(db: Session, owner_id: str, card_id: str):
        item = Item(owner_id=owner_id, card_id=card_id)
        db.add(item)
        db.commit()
        return item
    
    def get_cards_fav(db: Session, id: str):
        return db.query(Item).filter(Item.owner_id == id, Item.faved == True).all()

    def toggle_fav(db: Session, id: str):
        item = db.query(Item).filter(Item.id == id).first()
        item.faved = not item.faved
        db.commit()
        return item
        
        
