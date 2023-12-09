from beanie import PydanticObjectId
from pydantic import BaseModel

import schemes
import models


class CountryRepository:
    @staticmethod
    async def _get_with_project(country_id: str | PydanticObjectId, project: BaseModel):
        if isinstance(country_id, str):
            country_id = PydanticObjectId(country_id)

        return await models.Country.find_one(
            models.Country.id == country_id,
            projection_model=project
        )

    @staticmethod
    async def get(country_id: str | PydanticObjectId) -> models.Country | None:
        return await models.Country.find_one(
            models.Country.id == country_id
        )
    
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
    async def random(card_type: models.CardType, passed_cards: list[PydanticObjectId]) -> models.CountryShortView | None:
        country = await models.Country.aggregate([
            {
                "$unwind": "$cards"
            },
            {
                "$match": {
                    "_id": {"$nin": passed_cards},
                    "cards.type": card_type.value   
                }
            },
            {"$sample": {"size": 1}}
        ], projection_model=models.CountryShortView).to_list()
        if country:
            return country[0]
        return None


class UserRepository:

    @staticmethod
    async def get(user_id: str) -> models.UserData:
        user_data = await models.UserData.find_one({"user_id": user_id})

        if user_data is None:
            user_data = models.UserData(user_id=user_id)
            await user_data.save()

        return user_data

    @classmethod
    async def get_passed_cards(
            cls,
            user: models.UserData,
            card_type: models.CardType
    ) -> list[PydanticObjectId]:
        card_type_map = {
            models.CardType.ATTRACTIONS: user.passed_cards.attractions,
            models.CardType.NATIONAL_DISHES: user.passed_cards.national_dishes,
            models.CardType.CULTURAL_FEATURES: user.passed_cards.cultural_features,
            models.CardType.FACTS: user.passed_cards.facts,
            models.CardType.CREATIVITY: user.passed_cards.creativity
        }
        cards = card_type_map[card_type]
        return [PydanticObjectId(card) for card in cards]

    @classmethod
    async def add_passed_country_card(
            cls,
            user: models.UserData,
            country_id: str | PydanticObjectId,
            card_type: models.CardType
    ) -> None:
        if isinstance(country_id, PydanticObjectId):
            country_id = str(country_id)

        card_type_map = {
            models.CardType.ATTRACTIONS: user.passed_cards.attractions,
            models.CardType.NATIONAL_DISHES: user.passed_cards.national_dishes,
            models.CardType.CULTURAL_FEATURES: user.passed_cards.cultural_features,
            models.CardType.FACTS: user.passed_cards.facts,
            models.CardType.CREATIVITY: user.passed_cards.creativity
        }
        card = card_type_map[card_type]
        card.add(country_id)

        await user.save()

    @classmethod
    async def increase_score(
            cls,
            user: models.UserData,
            number: int
    ) -> int:
        user.score += number
        await user.save()

        return user.score

    @classmethod
    async def increase_global_score(
            cls,
            user: models.UserData
    ) -> int:
        user.global_score += user.score
        user.score = 0
        await user.save()

        return user.global_score

    @classmethod
    async def get_rank(cls, user: models.UserData) -> int | None:
        user_document_id = user.id

        rank = await user.aggregate(
            [
                {
                    '$sort': {
                        'global_score': -1
                    }
                }, {
                '$group': {
                    '_id': 'id',
                    'ids': {
                        '$push': '$_id'
                    }
                }
            }, {
                '$project': {
                    '_id': 0,
                    'index': {
                        '$indexOfArray': [
                            '$ids', user_document_id
                        ]
                    }
                }
            }
            ]
        ).to_list()
        if rank:
            return rank[0]["index"] + 1
        return None


if __name__ == '__main__':
    # aggregate
    # sort by score asc
    # set points_table index from 1 to ...
    import asyncio
    import random
    async def test():
        await models.init_database()

        user_id = "user-943"
        user = await UserRepository.get(user_id)
        rank = await UserRepository.get_rank(user)
        print(rank)

        # country_id = "6573288a542482462bcdfb8a"
        # await UserRepository.add_passed_country_card(user, country_id, models.CardType.ATTRACTIONS)
        #
        # print(user.passed_cards.attractions)
        # print(await UserRepository.card_is_passed(user, country_id, card_type=models.CardType.ATTRACTIONS))

        # for user in [f"user-{index}" for index in range(1000)]:
        #     user_id = user
        #     user = await UserRepository.get(user_id)
        #     await UserRepository.increase_score(user, random.randint(1, 1000))

    asyncio.run(test())
