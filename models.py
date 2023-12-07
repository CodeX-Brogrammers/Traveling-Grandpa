from typing import Optional, Union
import enum

from beanie import Document, Indexed, init_beanie, PydanticObjectId
from pydantic import BaseModel, conlist, model_validator, Field
from motor.motor_asyncio import AsyncIOMotorClient

from settings import settings


class Text(BaseModel):
    src: str
    tts: Optional[str]

    @model_validator(mode='before')
    def check_tts(cls, kwargs: dict):
        if kwargs.get("tts", None) is None:
            kwargs["tts"] = kwargs["src"]
        return kwargs


class Image(BaseModel):
    src: str
    yandex_id: str


class Answer(BaseModel):
    text: Text
    description: Text
    is_true: bool = False


class UserData(Document):
    user_id: Indexed(str, unique=True)
    passed_questions: list[PydanticObjectId] = Field(default_factory=list)

    @classmethod
    async def get_user_data(cls, user_id: str) -> "UserData":
        user_data = await cls.find_one({"user_id": user_id})

        if user_data is None:
            user_data = UserData(user_id=user_id)
            await user_data.save()

        return user_data

    async def add_passed_question(self, question_id: Union[str, PydanticObjectId]):
        if question_id not in self.passed_questions:
            if isinstance(question_id, str):
                question_id = PydanticObjectId(question_id)
            self.passed_questions.append(question_id)
            await self.save()


# Модель из БД
class Question(Document):
    full_text: Text
    short_text: Text
    hint: Text
    answers: conlist(Answer, max_length=3)
    image: Optional[Image]
    fact: Text

    class Settings:
        name = "Questions"


class CardType(str, enum.Enum):
    ATTRACTIONS = "Достопримечательность"
    NATIONAL_DISHES = "Национальные блюда"
    CULTURAL_FEATURES = "Культурные особенности"
    FACTS = "Факты о стране"
    CREATIVITY = "Творчество"


class CardAnswer(BaseModel):
    correct: Text
    incorrect: Text


class Card(BaseModel):
    type: CardType
    question: Text
    answers: CardAnswer
    image: Image | str | None = Field(None)


class Country(Document):
    names: list[str] = Field(..., description="Возможные наименование страны")
    facts: conlist(Text, max_length=3)
    hints: conlist(Text, max_length=3)
    cards: conlist(Card, max_length=5)

    class Settings:
        name = "Countries"


class CountryShortView(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    names: list[str]
    card: Card

    class Settings:
        projection = {"_id": 1, "names": 1, "card": "$cards"}


class CountryFacts(BaseModel):
    facts: conlist(Text, max_length=3)
    

class CountryHints(BaseModel):
    hints: conlist(Text, max_length=5)


async def init_database(*_):
    client = AsyncIOMotorClient(settings.mongodb_url)
    await init_beanie(database=client["QUEST"], document_models=[Question, UserData, Country])


# This is an asynchronous example, so we will access it from an async function
async def example():
    await init_database()
    
    data = await Country.aggregate([
        {
            "$unwind": "$cards"
        },
        {
            "$match": {
                "cards.type": CardType.ATTRACTIONS
            }
        },
        {"$sample": {"size": 1}}
    ], projection_model=CountryShortView).to_list()
    
    print(data)


if __name__ == "__main__":
    import asyncio
    asyncio.run(example())
    # CardType("")
    # print(CardType.__dict__)
    
