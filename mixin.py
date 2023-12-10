from typing import Callable
from functools import wraps

from aioalice.types import AliceRequest, AliceResponse
from aioalice import Dispatcher

from schemes import RepeatKey
from state import State


def mixin_can_repeat(dp: Dispatcher, key: RepeatKey = None):
    def inner(func: Callable):
        @wraps(func)
        async def wrapper(alice: AliceRequest, *args, **kwargs):
            nonlocal dp, key
            response = await func(alice, *args, **kwargs)
            data = await dp.storage.get_data(alice.session.user_id)
            data |= {"last": response, "last_func": func.__name__}
            if key:
                data[key] = response

            await dp.storage.set_data(
                alice.session.user_id, data
            )
            return response

        return wrapper

    return inner


def mixin_state(func: Callable):
    @wraps(func)
    async def wrapper(alice: AliceRequest, *args, **kwargs):
        if kwargs.get("state", None) is None:
            for value in args:
                if isinstance(value, State):
                    state = value
                    break
            else:
                state = State.from_request(alice)
                kwargs["state"] = state
        else:
            state = kwargs["state"]

        data = await func(alice, *args, **kwargs)
        if isinstance(data, dict):
            temp = data.copy()
            temp.pop("analytics")
            response = AliceResponse(**temp)
        else:
            response = data

        response.session_state = response.session_state | state.session.dict()
        response.user_state_update = response.user_state_update | state.user.dict()
        response.application_state = response.application_state | state.application
        if isinstance(data, AliceResponse):
            return response
        else:
            response = response.to_json()
            if events := data.get("analytics", {}).get("events", {}):
                if response.get("analytics", {}):
                    response["analytics"]["events"] += events
                else:
                    response["analytics"] = {}
                    response["analytics"]["events"] = events

            return response

    return wrapper


def mixin_appmetrica_log(dp: Dispatcher):
    def inner(func: Callable):
        @wraps(func)
        async def wrapper(alice: AliceRequest, *args, **kwargs):
            nonlocal dp
            state = State.from_request(alice)
            game_state = await dp.storage.get_state(alice.session.user_id, state)
            response: AliceResponse = await func(alice, *args, **kwargs)
            if isinstance(response, AliceResponse):
                response: dict = response.to_json()
            analytics = {
                "events": [
                    {
                        "name": func.__name__,
                        "value": {
                            "user": {
                                "id": alice.session.user_id,
                                "command": alice.request.command,
                                "intents": alice.request.nlu._raw_kwargs["intents"]
                            },
                            "game": {
                                "question_passed": state.session.question_passed,
                                "try_count": state.session.try_count
                            },
                            "state": game_state
                        }
                    }
                ]
            }
            if response.get("analytics", {}).get("events", {}):
                response["analytics"]["events"] += analytics["events"]
            else:
                response["analytics"] = analytics
            return response

        return wrapper

    return inner
