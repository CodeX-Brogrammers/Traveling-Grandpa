import enum

from aioalice.dispatcher.filters import Filter, check_filter, AsyncFilter
from aioalice.types import AliceRequest

import nlu


def _check_included_intent_names(alice: AliceRequest, intent_names: list[str]):
    intents: dict = alice.request.nlu._raw_kwargs["intents"]
    return any([intent_name in intents.keys() for intent_name in intent_names])


class NextFilter(Filter):
    def check(self, alice: AliceRequest):
        return _check_included_intent_names(alice, ["YANDEX.BOOK.NAVIGATION.NEXT"])


class ConfirmFilter(Filter):
    def check(self, alice: AliceRequest):
        return _check_included_intent_names(alice, ["YANDEX.CONFIRM", "YANDEX.BOOK.NAVIGATION.NEXT", "AGREE"])


class HintNeedFilter(Filter):
    def check(self, alice: AliceRequest):
        return _check_included_intent_names(alice, ["HINT_NEED"])


class RejectFilter(Filter):
    def check(self, alice: AliceRequest):
        return _check_included_intent_names(alice, ["YANDEX.REJECT", "REFUSAL"])


class RepeatFilter(Filter):
    def check(self, alice: AliceRequest):
        return _check_included_intent_names(alice, ["YANDEX.REPEAT", "REPEAT"])


class HelpFilter(Filter):
    SKIP_TOKENS = [
        nlu.lemmatize(["подсказка"])[0],
        nlu.lemmatize(["подсказать"])[0]
    ]

    def check(self, alice: AliceRequest):
        normalized_tokens = nlu.lemmatize(alice.request.nlu.tokens)
        return _check_included_intent_names(alice, ["YANDEX.HELP", "HELP"]) \
            and all([token not in normalized_tokens for token in self.SKIP_TOKENS])


class RestartFilter(Filter):
    def check(self, alice: AliceRequest):
        return _check_included_intent_names(alice, ["RESTART"])


class EndFilter(Filter):
    def check(self, alice: AliceRequest):
        return _check_included_intent_names(alice, ["END"])


class CanDoFilter(Filter):
    def check(self, alice: AliceRequest):
        return _check_included_intent_names(alice, ["WHATCANDO", "YANDEX.WHAT_CAN_YOU_DO"])


class DontKnowFilter(Filter):
    def check(self, alice: AliceRequest):
        return _check_included_intent_names(alice, ["DontKnow"])


class StartFilter(Filter):
    def check(self, alice: AliceRequest):
        return alice.session.new


class TextContainFilter(Filter):
    def __init__(self, initial_tokens: list[str]):
        self.init_tokens = nlu.lemmatize(initial_tokens)

    def check(self, alice: AliceRequest):
        user_tokens = nlu.lemmatize(
            nlu.tokenizer(alice.request.command)
        )
        return nlu.calculate_coincidence(user_tokens, self.init_tokens) > 0.75


class OneOfFilter(AsyncFilter):
    def __init__(self, *filters: Filter):
        self.filters = filters

    async def check(self, alice: AliceRequest):
        for filter in self.filters:
            if await check_filter(filter, (alice,)):
                return True
        return False


class AndFilter(AsyncFilter):
    def __init__(self, *filters: Filter):
        self.filters = filters

    async def check(self, alice: AliceRequest):
        result = []
        for filter in self.filters:
            result.append(await check_filter(filter, (alice,)))
        return all(result)


class SessionState(Filter):
    def __init__(self, state: str):
        self.state = state

    def check(self, alice: AliceRequest):
        state = alice._raw_kwargs["state"].get("session", {}).get("state", "*")
        return self.state == state
