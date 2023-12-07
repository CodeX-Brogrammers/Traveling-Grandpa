from random import choice, shuffle
from typing import Optional
import logging

from aioalice.types import AliceRequest, AliceResponse, Button
from aioalice.dispatcher.storage import MemoryStorage
from beanie import PydanticObjectId
from aioalice import Dispatcher


from nlu.cases import check_user_answer, SelectCardHandler, QuessAnswerHandler
from mixin import mixin_appmetrica_log, mixin_can_repeat, mixin_state
from state import State, GameStates
from schemes import RepeatKey, Diff
from const import (
    OK_BUTTON,
    REJECT_BUTTON,
    REPEAT_BUTTON,
    REPEAT_QUESTION_BUTTON,
    REPEAT_ANSWERS_BUTTON,
    YOU_CAN_BUTTON,
    HELP_BUTTON,
    HINT_BUTTON,
    NEXT_BUTTON,
    MENU_BUTTONS,
    GAME_BUTTONS,
    POSSIBLE_ANSWER,
    CONTINUE_ANSWER,
    FACT_ANSWER,
    SELECT_CARDS,
    SELECT_CARDS_ANSWERS
)
import repositories
import filters
import schemes
import models
import nlu


class HybridStorage(MemoryStorage):
    async def get_state(self, user_id, alice_state: State = None):
        if alice_state is None:
            return super().get_state(user_id)
        return alice_state.session.state

    async def set_state(self, user_id, state: str, alice_state: State = None):
        if alice_state is None:
            return super().set_state(user_id, state)
        alice_state.session.state = state


dp = Dispatcher(storage=HybridStorage())


@dp.request_handler(filters.StartFilter(), state="*")
@mixin_appmetrica_log(dp)
@mixin_can_repeat(dp)
@mixin_state
async def handler_start(alice: AliceRequest, state: State, **kwargs):
    logging.info(f"Handler->Старт")
    await dp.storage.set_state(
        alice.session.user_id,
        GameStates.START,
        alice_state=state
    )
    answer = "Уважаемые студенты, рада видеть вас на своей лекции. " \
             "Я профессор исторических наук, Аврора Хистория. " \
             "Вы можете узнать больше, если скажите \"Помощь\" и \"Что ты умеешь?\"" \
             "Я хочу поговорить с вами о том, как история может стать настоящей сказкой. " \
             "Что если я отправлю вас в настоящий мир фантазий и историй? " \
             "Я уже подготовила наш волшебный поезд. Чтобы начать лекцию просто скажите \"Поехали\". Готовы ли вы отправиться в это путешествие? "
    return alice.response_big_image(
        answer,
        tts=answer + '<speaker audio="dialogs-upload/97e0871e-cf33-4da5-9146-a8fa353b965e/9484707f-a9ae-4a1c-b8da-8111e026a9a8.opus">',
        image_id="213044/8caa36129ca6356f8981",
        buttons=MENU_BUTTONS,
        title="",
        description=answer
    )


@dp.request_handler(filters.EndFilter(), state="*")
@mixin_can_repeat(dp)
@mixin_appmetrica_log(dp)
async def handler_end(alice: AliceRequest, state: State = None, **kwargs):
    if state is None:
        state = State.from_request(alice)
    logging.info(f"User: {alice.session.user_id}: Handler->Заключение")
    await dp.storage.set_state(
        alice.session.user_id,
        GameStates.END,
        alice_state=state
    )
    text = "Что-ж мы прибываем на конечную станцию и наше путешествие подходит к концу. \n" \
           "Это было крайне увлекательно! \n" \
           "Я давно не встречала таких интересных людей, как вы! \n" \
           f"Вы ответили верно на {state.session.score} вопросов из {state.session.question_passed}. \n" \
           "Спасибо за наше путешествие. Возвращайтесь почаще, наш поезд всегда вас ждёт! \n" \
           "Желаете начать заново?"
    state.session.score = 0
    state.session.question_passed = 0
    return alice.response(
        text, buttons=[OK_BUTTON, REJECT_BUTTON],
        session_state=state.session.dict()
    )


@dp.request_handler(
    filters.ConfirmFilter(),
    filters.SessionState(GameStates.START),
    state="*"
)
@mixin_appmetrica_log(dp)
@mixin_can_repeat(dp)
@mixin_state
async def handler_start_game(alice: AliceRequest, state: State, **kwargs):
    logging.info(f"User: {alice.session.user_id}: Handler->Начать игру")
    return await handler_show_cards(alice, state=state)

# Отказ от игры и выход
@dp.request_handler(
    filters.RejectFilter(),
    filters.SessionState(GameStates.START),
    state="*"
)
@mixin_appmetrica_log(dp)
async def handler_reject_game(alice: AliceRequest, **kwargs):
    logging.info(f"User: {alice.session.user_id}: Handler->Отмена игры")
    answer = "Заходите почаще, всегда рад."
    return alice.response(answer, end_session=True)


@dp.request_handler(
    filters.SessionState(GameStates.SHOW_CARDS),
    state="*"
)
@mixin_appmetrica_log(dp)
@mixin_can_repeat(dp)
@mixin_state
async def handler_show_cards(alice: AliceRequest, state: State, extra_text: str = None, **kwargs):
    await dp.storage.set_state(
        alice.session.user_id,
        GameStates.SELECT_CARD,
        alice_state=state
    )

    return alice.response_items_list(
        text=extra_text if extra_text else "Выберите одну из карт",
        header="Выберите одну из карт",
        items=SELECT_CARDS
    )


@dp.request_handler(
    filters.SessionState(GameStates.SELECT_CARD),
    state="*"
)
@mixin_appmetrica_log(dp)
@mixin_state
async def handler_select_card(alice: AliceRequest, state: State, **kwargs):
    result = check_user_answer(alice, [
        SelectCardHandler(SELECT_CARDS_ANSWERS)
    ])
    if result is None or len(result) == 0:
        return await handler_show_cards(alice, state=state, extra_text="Не слышу, повтори ещё раз")

    if alice.request.type == "SimpleUtterance":
        answer: Diff = result[0]
        state.session.selected_card = models.CardType(answer.answer)
    else:
        state.session.selected_card = result

    return await handler_question(alice, state=state)


@dp.request_handler(
    filters.SessionState(GameStates.QUESTION_TIME),
    state="*"
)
@mixin_appmetrica_log(dp)
@mixin_can_repeat(dp, RepeatKey.QUESTION)
@mixin_state
async def handler_question(alice: AliceRequest, state: State, **kwargs):
    selected_card = state.session.selected_card
    # TODO: запоминать пройденные типы карточек
    user_data = await models.UserData.get_user_data(alice.session.user_id)
    country = await repositories.CountryRepository.random(
        card_type=selected_card,
        passed_questions=user_data.passed_questions
    )
    
    if country is None:
        return await handler_show_cards(alice, state=state, extra_text="Повтори ещё раз")
    card = country.card
    print(f"Country: {country.names}")
    state.session.current_question = str(country.id)
    await dp.storage.set_state(
        alice.session.user_id,
        GameStates.GUESS_ANSWER,
        alice_state=state
    )
    
    return alice.response_big_image(
        text=card.question.src,
        tts=card.question.tts,
        image_id=card.image,
        title="",
        description=card.question.src
    )


@dp.request_handler(
    filters.SessionState(GameStates.GUESS_ANSWER),
    state="*"
)
@mixin_can_repeat(dp)
@mixin_state
async def handler_quess_answer(alice: AliceRequest, state: State):
    country_id = state.session.current_question
    selected_card = state.session.selected_card
    country = await repositories.CountryRepository.get_card_with_names(
        country_id=country_id,
        card_type=selected_card
    )
    
    if country is None:
        pass
    print(country)
    possible_answers = [schemes.AnswerWithIndex(index=0, text=name) for name in country.names]

    result = check_user_answer(alice, handlers=[QuessAnswerHandler(
        answers=possible_answers
    )])

    if result is None:
        return await handler_false_answer(alice, state=state)

    first_country: Diff = result[0]
    if first_country.coincidence >= 0.5:
        return await handler_true_answer(alice, state=state)

    return await handler_show_cards(alice, state=state)


@mixin_state
async def handler_false_answer(alice: AliceRequest, state: State, **kwargs):
    state.session.try_number += 1

    if state.session.try_number >= 3:
        return await handler_show_cards(alice, state=state)
    return alice.response("Не угадал, попробуй ещё раз")


@mixin_state
async def handler_true_answer(alice: AliceRequest, state: State, **kwargs):
    state.session.try_number = 0

    return await handler_show_cards(alice, state=state)


@dp.errors_handler()
@mixin_appmetrica_log(dp)
async def the_only_errors_handler(alice, e):
    logging.error('An error!', exc_info=e)
    return alice.response('Кажется что-то пошло не так. ')
