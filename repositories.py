from aioalice.types import Image, Button
from beanie import PydanticObjectId
from pydantic import BaseModel

import models
import schemes
import nlu


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
    async def get_card_with_names(
            country_id: str | PydanticObjectId, card_type: models.CardType
    ) -> models.CountryShortView | None:
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
    async def random(card_type: models.CardType,
                     passed_cards: list[PydanticObjectId]) -> models.CountryShortView | None:
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

    @staticmethod
    async def count() -> int:
        country = await models.Country.aggregate([
            {"$count": "count"}
        ]).to_list()
        if country:
            return country[0]["count"]
        return 0

    @staticmethod
    async def get_countries_names() -> dict | None:
        countries = await models.Country.aggregate([
            {
                '$project': {
                    '_id': 0,
                    'names': '$alternatives'
                }
            }
        ]).to_list()
        if not countries:
            return None

        result = dict()
        for country in countries:
            names = [nlu.lemmatize([name])[0] for name in country["names"]]
            country = names[0]
            for name in names:
                result[name] = country
        return result


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
    async def get_passed_cards_count(
            cls,
            user: models.UserData
    ) -> schemes.PassedCardCountView | None:
        result = await models.UserData.aggregate([
            {
                '$match': {
                    'user_id': user.user_id
                }
            }
        ], projection_model=schemes.PassedCardCountView).to_list()
        if result:
            return result[0]
        return None

    @classmethod
    async def clear_passed_cards(
            cls,
            user: models.UserData
    ) -> None:
        user.passed_cards.attractions = set()
        user.passed_cards.national_dishes = set()
        user.passed_cards.cultural_features = set()
        user.passed_cards.facts = set()
        user.passed_cards.creativity = set()
        await user.save()

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


class CardRepository:
    CARDS = {
        models.CardType.ATTRACTIONS: Image(
            image_id="997614/8e4eda6eb11d49980d4d",
            title="Достопримечательности",
            description="Здесь вам предстоит увлекательное путешествие по всему миру, "
                        "отгадывайте страны на основе их знаменитых архитектурных и природных чудес.",
            button=Button(
                title="Достопримечательности",
                payload={
                    "selected_card": models.CardType.ATTRACTIONS,
                    "tts": '<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/667c77d3-88b8-4b37-88c1-b6cbc636cfda.opus">'
                }
            )
        ),
        models.CardType.NATIONAL_DISHES: Image(
            image_id="1540737/f91ca46e2da86edffc96",
            title="Национальные блюда",
            description="Угадывайте страны, открывая для себя удивительное разнообразие мировой кухни и "
                        "наслаждайтесь любимыми национальными блюдами из разных стран.",
            button=Button(
                title="Национальные блюда",
                payload={
                    "selected_card": models.CardType.NATIONAL_DISHES,
                    "tts": '<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/c14edaf5-1d69-40da-b8cf-c29e422ece7f.opus">'
                }
            )
        ),
        models.CardType.CULTURAL_FEATURES: Image(
            image_id="997614/6b6b4fb3948f86b612e8",
            title="Культурные особенности",
            description="Угадывайте страны, исследуя их традиции, праздники, "
                        "исторические артефакты и другие интересные аспекты.",
            button=Button(
                title="Культурные особенности",
                payload={
                    "selected_card": models.CardType.CULTURAL_FEATURES,
                    "tts": '<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/f1f46843-c453-4fae-916a-d94cc6a1b0c7.opus">'
                }
            )
        ),
        models.CardType.FACTS: Image(
            image_id="997614/6af22da7d2ef486a58e8",
            title="Факты о стране",
            description="Здесь вам предстоит угадывать страны, "
                        "исходя из удивительных фактов о их географии, культуре и истории.",
            button=Button(
                title="Факты о стране",
                payload={
                    "selected_card": models.CardType.FACTS,
                    "tts": '<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/54c12ab7-255f-40ec-a6fd-283d4945bc72.opus">'
                }
            )
        ),
        models.CardType.CREATIVITY: Image(
            image_id="1652229/06aa85c89296ea2dd776",
            title="Творчество",
            description="Откройте для себя мир творчества, отгадывайте страны через их художественное"
                        " наследие, литературные достижения и культурные выражения.",
            button=Button(
                title="Творчество",
                payload={
                    "selected_card": models.CardType.CREATIVITY,
                    "tts": '<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/242705b0-f065-4693-b39d-271e6df9ff5a.opus">'
                }
            )
        )
    }

    @classmethod
    async def get(cls, user: models.UserData) -> list[Image]:
        countries_count: int = await CountryRepository.count()
        cards_type_passed: schemes.PassedCardCountView = await UserRepository.get_passed_cards_count(user)
        cards_type_passed: dict = cards_type_passed.model_dump()

        result = []
        for card_type in models.CardType:
            card = cls.CARDS[card_type]
            pass_count = cards_type_passed[card_type.name.lower()]
            if pass_count < countries_count:
                result.append(card)

        return result

    @staticmethod
    def calculate_answers_with_index(cards: list[Image]) -> list[schemes.AnswerWithIndex]:
        result = []
        for index, card in enumerate(cards, start=1):
            result.append(schemes.AnswerWithIndex(
                index=index,
                text=models.CardType(card.title).value
            ))
        return result


if __name__ == '__main__':
    # aggregate
    # sort by score asc
    # set points_table index from 1 to ...
    import asyncio
    import random


    async def test():
        await models.init_database()

        # user_id = "0949EEBA2D0E3A59ED6052A46EFC046E6CD43719F826539F1137AED6A7383B09"
        # user = await UserRepository.get(user_id)
        # cards = await CardRepository.get(user)
        # answers = CardRepository.calculate_answers_with_index(cards)
        # print(answers)
        names = await CountryRepository.get_countries_names()
        print(names)
        # rank = await UserRepository.get_rank(user)
        # print(rank)

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
