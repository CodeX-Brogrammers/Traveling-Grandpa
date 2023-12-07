from beanie import PydanticObjectId
from pydantic import BaseModel

import schemes
import models


class CountryRepository:
    @staticmethod
    async def _get_with_project(country_id: str | PydanticObjectId, project: BaseModel) -> BaseModel | None:
        return await models.Country.find_one(
            models.Country.id == country_id, 
            projection_model=project
        )
    
    @staticmethod
    async def get(country_id: str | PydanticObjectId) -> models.Country | None:
        return await models.Country.find_one(models.Country.id == country_id)
    
    @staticmethod
    async def get_card_with_names(country_id: str | PydanticObjectId, card_type: models.CardType) -> models.CountryShortView | None:
        country = await models.Country.aggregate([
            {
                "$unwind": "$cards"
            },
            {
                "$match": {
                    "_id": PydanticObjectId(country_id),
                    "cards.type": {"$eq": card_type.value}
                }
            },
            {"$sample": {"size": 1}}
        ], projection_model=models.CountryShortView).to_list()

        if country:
            return country[0]
        return None
    
    @classmethod
    async def get_facts(cls, country_id: str | PydanticObjectId) -> models.CountryFacts | None:
        return await cls._get_with_project(
            country_id=country_id, 
            project=models.CountryFacts
        )
    
    @classmethod
    async def get_hints(cls, country_id: str | PydanticObjectId) -> models.CountryHints | None:
        return await cls._get_with_project(
            country_id=country_id, 
            project=models.CountryHints
        )
    
    @staticmethod
    async def random(card_type: models.CardType, passed_questions: list[str]) -> models.CountryShortView | None:
        country = await models.Country.aggregate([
            {
                "$unwind": "$cards"
            },
            {
                "$match": {
                    "_id": {"$nin": passed_questions},
                    "cards.type": card_type.value   
                }
            },
            {"$sample": {"size": 1}}
        ], projection_model=models.CountryShortView).to_list()
        if country:
            return country[0]
        return None
