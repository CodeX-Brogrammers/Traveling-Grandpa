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


# Обработчик повторения последней команды
@dp.request_handler(filters.RepeatFilter(), state="*")
@mixin_appmetrica_log(dp)
@mixin_state
async def handler_repeat(alice: AliceRequest, state: State):
    return alice.response("Повторять нечего")


@dp.request_handler(filters.CanDoFilter(), state="*")
@mixin_appmetrica_log(dp)
@mixin_can_repeat(dp)
@mixin_state
async def handler_can_do(alice: AliceRequest, state: State, **kwargs):
    logging.info(f"User: {alice.session.user_id}: Handler->Что ты умеешь")
    answer = "Всё умею"
    return alice.response(answer)


@dp.request_handler(filters.HelpFilter(), state="*")
@mixin_appmetrica_log(dp)
@mixin_can_repeat(dp)
@mixin_state
async def handler_help(alice: AliceRequest, state: State, **kwargs):
    logging.info(f"User: {alice.session.user_id}: Handler->Помощь")
    fsm_state = await dp.storage.get_state(alice.session.user_id, state)
    if fsm_state.upper() in ("GUESS_ANSWER", "FACT", "QUESTION_TIME"):
        answer = "В данный момент вы можете попросить меня о следующем: \n" \
                 "1. Повтори - повторю свой последний ответ \n" \
                 "2. Повтори вопрос \n" \
                 "3. Подсказка \n" \
                 "4. Сколько осталось подсказок \n" \
                 "5. Пропустить вопрос - если вопрос сложный, то так уж и быть пропустим его \n" \
                 "6. Перезапуск - начнем с начала \n" \
                 "7. Выход - мы остановим лекцию и вы спокойно сможете идти по своим делам \n"
        return alice.response(
            answer,
            buttons=[
                REPEAT_QUESTION_BUTTON,
                REPEAT_ANSWERS_BUTTON,
                *GAME_BUTTONS
            ]
        )

    # TODO: Заменить базовый текст помощи, он не напоминает помощь
    answer = "Тут будет помощь"
    if fsm_state.upper() in ("START", "*"):
        answer = f"{answer}\n{choice(POSSIBLE_ANSWER)}"
        return alice.response(answer, buttons=MENU_BUTTONS)
    return alice.response(answer)


@dp.request_handler(filters.RestartFilter(), state="*")
@mixin_appmetrica_log(dp)
async def handler_restart(alice: AliceRequest, **kwargs):
    return await handler_start(alice)


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
    filters.ConfirmFilter(),
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
    filters.SessionState(GameStates.SHOW_CARDS),
    filters.RejectFilter(),
    state="*"
)
@mixin_appmetrica_log(dp)
@mixin_can_repeat(dp)
@mixin_state
async def handler_reject_game(alice: AliceRequest, state: State):
    return await handler_end(alice, state=state)


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
    state.clear_after_question()
    
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
    filters.OneOfFilter(
        filters.NextFilter(),
        filters.TextContainFilter(["следующий", "вопрос"]),
        filters.TextContainFilter(["пропустить", "вопрос"]),
    ),
    filters.SessionState(GameStates.GUESS_ANSWER),
    state="*"
)
@mixin_appmetrica_log(dp)
async def handler_skip_question(alice: AliceRequest):
    return await handler_show_cards(alice)


@dp.request_handler(
    filters.OneOfFilter(
        # filters.DontKnowFilter(),
        filters.TextContainFilter(["не", "знаю"]),
        filters.TextContainFilter(["не", "могу"]),
        filters.TextContainFilter(["сложно"]),
        filters.TextContainFilter(["без", "понятия"]),
        filters.TextContainFilter(["понятия", "не", "имею"]),
    ),
    filters.SessionState(GameStates.GUESS_ANSWER),
    state="*"
)
@mixin_appmetrica_log(dp)
async def handler_dont_know_answer(alice: AliceRequest):
    text = "Мы многого не знаем, попробуйте взять подсказку или перейдите на следующий вопрос. "
    return alice.response(text, buttons=GAME_BUTTONS)


@dp.request_handler(
    filters.TextContainFilter(["подсказка"]),
    filters.OneOfFilter(
        filters.SessionState(GameStates.GUESS_ANSWER)
    ),
    state="*"
)
@mixin_appmetrica_log(dp)
@mixin_can_repeat(dp, RepeatKey.HINT)
@mixin_state
async def handler_hint(alice: AliceRequest, state: State, **kwargs):
    country_id = state.session.current_question
    selected_card = state.session.selected_card
    
    if state.session.number_of_hints <= 0:
        return alice.response("Извини внучок, у тебя больше нет подсказок")
    
    elif len(state.session.latest_hints) >= 3:
        return alice.response("Извини внучок, ты получил все подсказки об этой стране")
    
    country: models.CountryHints = await repositories.CountryRepository.get_hints(
        country_id=country_id,
        card_type=selected_card
    )
    
    hints: list[schemes.AnswerWithIndex] = [
        schemes.AnswerWithIndex(index=index, text=hint) 
        for index, hint in enumerate(country.hints, 1)
    ]
    
    for _hint in hints:
        if _hint.index in state.session.latest_hints:
            continue
        
        hint = choice(hints)
        state.session.latest_hints.append(hint.index)
    
    state.session.number_of_hints -= 1
    return alice.response(
        hint.text.src,
        tts=hint.text.tts
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


# TODO
# @mixin_appmetrica_log(dp)
# @mixin_state
# async def handler_answer_brute_force(alice: AliceRequest, state: State, **kwargs):
#     logging.info(f"User: {alice.session.user_id}: Handler->Перебор ответов")


@mixin_state
async def handler_true_answer(alice: AliceRequest, state: State, **kwargs):
    state.session.try_number = 0

    return await handler_show_cards(alice, state=state)


@mixin_state
async def handler_false_answer(alice: AliceRequest, state: State, **kwargs):
    state.session.try_number += 1

    if state.session.try_number >= 3:
        return await handler_show_cards(alice, state=state)
    return alice.response("Не угадал, попробуй ещё раз")


@dp.request_handler(
    filters.ConfirmFilter(),
    filters.SessionState(GameStates.FACT),
    state="*")
@mixin_appmetrica_log(dp)
@mixin_can_repeat(dp)
@mixin_state
async def handler_fact_confirm(alice: AliceRequest, state: State, **kwargs):
    logging.info(f"User: {alice.session.user_id}: Handler->Отправка факта")
    
    country_id = state.session.current_question
    country: models.CountryFacts = await repositories.CountryRepository.get_facts(
        country_id=country_id
    )
    
    await dp.storage.set_state(
        alice.session.user_id,
        state=GameStates.QUESTION_TIME,
        alice_state=state
    )
    
    fact: schemes.Text = choice(country.facts)
    return alice.response(
        fact.src,
        tts=fact.tts,
        buttons=[OK_BUTTON, REJECT_BUTTON]
    )


@dp.request_handler(
    filters.RejectFilter(),
    filters.SessionState(GameStates.FACT),
    state="*"
)
@mixin_appmetrica_log(dp)
@mixin_can_repeat(dp)
async def handler_fact_reject(alice: AliceRequest, **kwargs):
    logging.info(f"User: {alice.session.user_id}: Handler->Отказ от факта")
    return await handler_show_cards(alice)


@dp.errors_handler()
@mixin_appmetrica_log(dp)
async def the_only_errors_handler(alice, e):
    logging.error('An error!', exc_info=e)
    return alice.response('Кажется что-то пошло не так. ')
