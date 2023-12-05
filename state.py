from typing import Optional

from aioalice.utils.helper import Helper, HelperMode, Item
from pydantic import BaseModel, conint, Field
from aioalice.types import AliceRequest

from models import CardType


class SessionState(BaseModel):
    selected_card: Optional[CardType] = None
    current_question: Optional[str] = None
    question_passed: Optional[conint(ge=0)] = Field(0)
    number_of_hints: int = 5
    try_number: int = 0
    score: Optional[conint(ge=0)] = Field(0)
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
