from dataclasses import dataclass
from typing import Optional
import enum

from pydantic import BaseModel, Field


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


class AnswerWithIndex(BaseModel):
    index: int | None = Field(None)
    text: str = Field(...)
