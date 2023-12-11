from typing import Optional
import enum

from aioalice.utils.helper import Helper, HelperMode, Item
from aioalice.dispatcher.storage import MemoryStorage
from pydantic import BaseModel, conint, Field
from aioalice.types import AliceRequest
from redis import asyncio as aioredis
import orjson

from settings import settings
from models import CardType


class SessionState(BaseModel):
    selected_card: Optional[CardType] = None
    current_question: Optional[str] = None
    question_passed: Optional[conint(ge=0)] = Field(default=0)
    latest_hints: list[int] = Field(default_factory=list)
    try_count: int = 0
    need_hint: bool = Field(default=False)
    need_repeat: bool = Field(default=False)
    state: str = "*"


class UserState(BaseModel):
    score: Optional[conint(ge=0)] = Field(0)


class State(BaseModel):
    session: SessionState = SessionState()
    user: UserState = UserState()
    application: dict = Field(default_factory=dict)

    @classmethod
    def from_request(cls, alice: AliceRequest):
        return cls(**alice._raw_kwargs["state"])

    @property
    def current(self) -> str:
        return self.session.state
    
    def clear_after_question(self) -> None:
        self.session.latest_hints = []
        self.session.try_count = 0
        self.session.need_hint = False


class GameStates(Helper):
    mode = HelperMode.snake_case

    START = Item()  # Навык только запустился
    SHOW_CARDS = Item()  # Показ карточек
    SELECT_CARD = Item()  # Выбор карточки
    QUESTION_TIME = Item()  # Время вопроса
    GUESS_ANSWER = Item()  # Выбор ответов
    FACT = Item()  # Выбор ответов
    HINT = Item()  # Подсказка
    END = Item()  # Завершение


def json_deserialization(obj):
    if any([
        "Alice" in str(type(obj)),
        "Card" in str(type(obj)),
        "Image" in str(type(obj)),
        "Button" in str(type(obj)),
    ]):
        return obj.to_json()
    elif isinstance(obj, enum.Enum):
        return obj.value
    raise TypeError


class HybridStorage(MemoryStorage):
    def __init__(self):
        self.redis: aioredis.Redis | None = None
        if settings.redis_enable:
            self.redis: aioredis.Redis = aioredis.from_url(url=settings.redis_url)

        super().__init__()

    async def _get_user_data(self, user_id):
        if self.redis:
            data = await self.redis.get(user_id)
            data = orjson.loads(data)
            if not data:
                data = {}
                await self.redis.set(user_id, "{}", ex=60 * 5)

            return data

        if user_id not in self.data:
            self.data[user_id] = {}
        return self.data[user_id]

    async def get_data(self, user_id):
        user = await self._get_user_data(user_id)
        return user

    async def reset_data(self, user_id):
        if self.redis:
            await self.redis.set(user_id, "{}")

    async def set_data(self, user_id, data):
        userdata = await self._get_user_data(user_id)
        userdata.update(data)
        userdata = orjson.dumps(userdata, default=json_deserialization)
        if self.redis:
            await self.redis.set(user_id, userdata)

    async def get_state(self, user_id, state: State = None):
        if state is None:
            return super().get_state(user_id)
        return state.current

    async def set_state(self, user_id, state: str, alice_state: State = None):
        if alice_state is None:
            return super().set_state(user_id, state)
        alice_state.session.state = state
