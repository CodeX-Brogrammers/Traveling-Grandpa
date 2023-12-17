import logging
import json

from aiohttp.web_response import Response
from aiohttp.web_request import Request
from aiohttp import web

from repositories import AnswersCollectorRepository
from state import SessionState


@web.middleware
async def only_post_request_middleware(request: Request, handler):
    if request.method.upper() != "POST":
        return Response(status=403)
    return await handler(request)


@web.middleware
async def ping_request_middleware(request: Request, handler):
    data = await request.json()
    if data.get("request", {}).get("original_utterance", None) == "ping":
        return web.json_response({"text": "pong"})
    return await handler(request)


@web.middleware
async def log_middleware(request: Request, handler):
    data = await request.json()
    _request = data["request"]
    user_id = data.get('session', {}).get('user_id', 0)
    user_fsm_state = data.get("state", {}).get("session", {}).get("state", None)
    logging.info(
        f"User ({user_id}) enter"
        f"\nCommand: {_request.get('command', None)}"
        f"\nToken: {_request.get('nlu', {}).get('tokens', None)}"
        f"\nIntents: {_request.get('nlu', {}).get('intents', None)}"
        f"\nFSM State: {user_fsm_state}"
    )
    response = await handler(request)
    logging.info(
        f"User ({user_id}) exit"
        f"\nFSM State: {user_fsm_state}"
    )
    return response


@web.middleware
async def session_state_middleware(request, handler):
    response = await handler(request)
    data = (await request.json()).get("state", {}).get("session", {})
    if not data:
        return response

    state = SessionState(**data).model_dump()
    body = json.loads(response.body)
    body_state = body.get("session_state", {})
    if isinstance(state, dict) and isinstance(body_state, dict):
        body["session_state"] = state | body.get("session_state", {})
    else:
        body["session_state"] = state

    response.body = json.dumps(body)
    return response


@web.middleware
async def answers_collector_middleware(request: Request, handler):
    data = await request.json()

    session = data.get("state", {}).get("session", {})
    current_state = session.get("state", None)
    previous_state = session.get("previous_state", None)

    request_obj = data.get("request", {})
    answer = request_obj.get("command", None)

    if answer:
        try:
            await AnswersCollectorRepository.add(
                current_state=current_state,
                previous_state=previous_state,
                answer=answer
            )
        except Exception as ex:
            logging.error(str(ex))

    return await handler(request)
