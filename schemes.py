from dataclasses import dataclass
from typing import Optional
import enum

from pydantic import BaseModel, Field, model_validator


class RepeatKey(enum.Enum):
    LAST = "last"
    HINT = "hint"
    QUESTION = "question"


@dataclass(slots=True, frozen=True)
class CleanAnswer:
    src: str
    clean: list[str]
    number: int


@dataclass(slots=True, frozen=True)
class Diff:
    answer: str
    number: int
    coincidence: float


@dataclass(slots=True, frozen=True)
class UserCheck:
    diff: Optional[Diff] = None
    is_true_answer: bool = False


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


class AnswerWithIndex(BaseModel):
    index: int | None = Field(None)
    text: str | Text = Field(...)
