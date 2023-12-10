from typing import Optional, Union, Any
import enum

from beanie import Document, Indexed, init_beanie, PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, conlist, Field

from schemes import Image, Text
from settings import settings


class CardType(str, enum.Enum):
    ATTRACTIONS = "Достопримечательности"
    NATIONAL_DISHES = "Национальные блюда"
    CULTURAL_FEATURES = "Культурные особенности"
    FACTS = "Факты о стране"
    CREATIVITY = "Творчество"

    @classmethod
    def _missing_(cls, value: str | Any) -> "CardType":
        if not isinstance(value, str):
            raise ValueError(f"Only the string is allowed, given type: {type(value)}")

        const_names_map = cls._member_map_
        value = value.upper()
        if card := const_names_map.get(value, None):
            return card

        raise ValueError(f"Name: {value} not found")


class CardAnswer(BaseModel):
    correct: Text
    incorrect: Text


class Card(BaseModel):
    type: CardType
    question: Text
    answers: CardAnswer
    image: Image | str | None = Field(None)


class Country(Document):
    name: str = Field(...)
    alternatives: list[str] = Field(..., description="Возможные наименование страны")
    facts: conlist(Text, max_length=3)
    hints: conlist(Text, max_length=3)
    cards: conlist(Card, max_length=5)

    class Settings:
        name = "Countries"
        use_cache = True
        cache_capacity = 50


class CountryShortView(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    alternatives: list[str]
    card: Card
    name: str

    class Settings:
        projection = {
            "_id": 1,
            "alternatives": 1,
            "card": "$cards",
            "name": 1
        }


class CountryFacts(BaseModel):
    facts: conlist(Text, max_length=3)
    

class CountryHints(BaseModel):
    hints: conlist(Text, max_length=5)


class PassedCard(BaseModel):
    attractions: set[str] = Field(default_factory=set)
    national_dishes: set[str] = Field(default_factory=set)
    cultural_features: set[str] = Field(default_factory=set)
    facts: set[str] = Field(default_factory=set)
    creativity: set[str] = Field(default_factory=set)


class UserData(Document):
    user_id: Indexed(str, unique=True)
    passed_cards: PassedCard = Field(default_factory=PassedCard)
    score: int = Field(default=0)
    global_score: int = Field(default=0)


async def init_database(*_):
    client = AsyncIOMotorClient(settings.mongodb_url)
    await init_beanie(database=client["QUEST"], document_models=[UserData, Country])
