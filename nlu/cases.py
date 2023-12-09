from operator import attrgetter
from typing import Any

from aioalice.types import AliceRequest

from schemes import Diff, CleanAnswer, AnswerWithIndex
from state import State, GameStates
from models import CardType
import nlu


def _remove_common_words_from_answers(answers: list[AnswerWithIndex]) -> list[CleanAnswer]:
    result = []
    for answer in answers:
        normalized_answer = nlu.lemmatize(nlu.tokenizer(answer.text))
        result.append(
            CleanAnswer(
                number=answer.index,
                src=answer.text,
                clean=nlu.remove_common_words(
                    normalized_answer
                )
            )
        )
    return result


def _calculate_correct_answer(
        user_answer: str, answers: list[CleanAnswer], by_number: bool = False, threshold: float = 0.33) -> list[Diff]:
    result = []
    normalized_user_answer = set(nlu.lemmatize(nlu.tokenizer(user_answer)))
    for answer in answers:
        if by_number and answer.number != 0:
            normalized_answer = set(str(answer.number))
        else:
            normalized_answer = set(answer.clean)

        coincidence = nlu.calculate_coincidence(normalized_user_answer, normalized_answer)
        if coincidence >= threshold:
            result.append(
                Diff(
                    answer=answer.src,
                    number=answer.number,
                    coincidence=coincidence
                )
            )
    result.sort(key=attrgetter("coincidence"), reverse=True)
    return result


def _clean_user_command(command: str, answers: list[CleanAnswer], exclude_tokens: list[str] | None = None) -> str:
    user_answer_tokens = nlu.lemmatize(nlu.tokenizer(command))
    common_words = set()
    if exclude_tokens:
        for token in set(exclude_tokens):
            common_words.add(token)

    result = nlu.remove_common_words(user_answer_tokens)

    skip_index = set()
    text_enters = []
    for answer in answers:
        indexs = nlu.find_occurrences(result, answer.clean, skip_index)
        text_enters.append(indexs)
        skip_index.symmetric_difference_update(indexs)

    for answer in answers:
        text_enters = nlu.find_occurrences(result, [*answer.clean, str(answer.number)])
        to_exclude = nlu.exclude_words(result, text_enters)
        if to_exclude:
            for number in text_enters:
                result[number] = "*"

    return " ".join(result)


def check_user_answer(alice: AliceRequest, handlers: list["BaseHandler"]) -> Any:
    for handler in handlers:
        handler.set_alice(alice)
        if handler.condition():
            return handler.execute()


class BaseHandler:
    def __init__(self, answers: list[AnswerWithIndex]):
        self.alice = None
        self.answers = answers

    def set_alice(self, alice: AliceRequest):
        self.alice = alice

    def text(self, exclude_tokens: list[str] | None = None, skip_number_check: bool = False) -> list[Diff] | None:
        answers = _remove_common_words_from_answers(self.answers)
        user_answer = _clean_user_command(
            command=self.alice.request.command,
            answers=answers,
            exclude_tokens=exclude_tokens
        )
        conditions = [False] if skip_number_check else [True, False]
        for condition in conditions:
            diffs = _calculate_correct_answer(
                user_answer, answers, by_number=condition
            )
            if len(diffs) >= 1:
                return diffs
        return None

    def condition(self) -> bool:
        raise NotImplementedError("")

    def execute(self) -> Any:
        raise NotImplementedError("")


class SelectCardHandler(BaseHandler):
    def condition(self) -> bool:
        state = State.from_request(self.alice)
        return state.current == GameStates.SELECT_CARD

    def button(self) -> CardType:
        return CardType(self.alice.request.payload["selected_card"])

    def execute(self) -> list[Diff] | CardType | None:
        if self.alice.request.type == "ButtonPressed":
            return self.button()

        return self.text(exclude_tokens=["о"])


class QuessAnswerHandler(BaseHandler):
    def condition(self) -> bool:
        state = State.from_request(self.alice)
        return state.current == GameStates.GUESS_ANSWER

    def execute(self) -> list[Diff] | None:
        return self.text(skip_number_check=True)
