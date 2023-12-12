from random import choice
import logging

from aioalice.types import AliceRequest, Image, AliceResponse
from aioalice import Dispatcher

from nlu.cases import check_user_answer, SelectCardHandler, QuessAnswerHandler
from mixin import mixin_appmetrica_log, mixin_can_repeat, mixin_state
from state import State, GameStates, HybridStorage
from schemes import RepeatKey, Diff
from const import (
    DONT_KNOW, FACT_ANYTHING_ELSE_MOMENT,
    SELECT_CARD_ANYTHING_ELSE_MOMENT,
    NEW_OR_CLOSE_GAME_BUTTONS_GROUP,
    REPEAT_OR_CLOSE_BUTTONS_GROUP,
    CONTINUE_ANYTHING_ELSE_MOMENT,
    INCORRECT_ANSWERS_COUNTRY,
    END_ANYTHING_ELSE_MOMENT,
    CONFIRM_BUTTONS_GROUP,
    MENU_BUTTONS_GROUP,
    ALL_HINTS_IS_TAKES,
    GAME_BUTTONS_GROUP,
    INCORRECT_ANSWERS,
    HINT_DONT_NEED,
    REPEAT_PLEASE, SHOW_CARDS_ANSWER, START_ANSWER,
)
import repositories
import filters
import schemes
import models
import nlu

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
    await dp.storage.reset_data(alice.session.user_id)

    answer = START_ANSWER
    return alice.response_big_image(
        answer.src,
        tts=answer.tts,
        image_id="1652229/066bed1b217f0e2c894a",
        buttons=MENU_BUTTONS_GROUP,
        title="",
        description=answer.src
    )


@dp.request_handler(
    filters.TextContainFilter(["алиса"]),
    filters.SessionState(GameStates.START),
    state="*"
)
@mixin_appmetrica_log(dp)
async def handler_new_game(alice: AliceRequest, **kwargs):
    return alice.response(
        "ЧТО-ТО",
        tts="""
        <speaker audio="dialogs-upload/936e66b3-1d74-4b8a-8a97-2a31f8367fb4/6efc7e21-4f28-438f-b3bb-8585d0c14dd9.opus">
        <speaker audio="dialogs-upload/936e66b3-1d74-4b8a-8a97-2a31f8367fb4/f0b8e03c-7cb0-446c-9c7e-e19dc4133f26.opus">
        Это самый короткий путь до аэропорта по версии Яндекс карт.
        <speaker audio="alice-sounds-things-phone-1.opus">
        <speaker audio="dialogs-upload/936e66b3-1d74-4b8a-8a97-2a31f8367fb4/7acc4e36-471a-47a0-9883-3d3f3b17344a.opus">
        Привет, мы рады тебя снова видеть, мы вот вот отправимся в новое путешествие ты с нами ?
        """
    )


@dp.request_handler(
    filters.SessionState(GameStates.END),
    filters.OneOfFilter(
        filters.ConfirmFilter(),
        filters.TextContainFilter(["Новая", "игра"]),
        filters.TextContainFilter(["сначала"]),
    ),
    state="*"
)
@mixin_appmetrica_log(dp)
async def handler_new_game(alice: AliceRequest, **kwargs):
    return await handler_show_cards(alice)


@dp.request_handler(
    filters.SessionState(GameStates.END),
    filters.OneOfFilter(
        filters.EndFilter(),
        filters.RejectFilter(),
        filters.TextContainFilter(["Выход"]),
        filters.TextContainFilter(["Хватит"]),
        filters.TextContainFilter(["Закрыть"])
    ),
    state="*"
)
@mixin_appmetrica_log(dp)
async def handler_close_game(alice: AliceRequest, text: str | None = None, **kwargs):
    close_text = "Буду скучать, возвращайся! С любовью, твой дедушка ♥"
    if text:
        close_text = text + close_text

    return alice.response(
        close_text,
        end_session=True
    )


@dp.request_handler(
    filters.OneOfFilter(
        filters.EndFilter(),
        filters.AndFilter(
            filters.SessionState(GameStates.SHOW_CARDS),
            filters.RejectFilter()
        )
    ),
    state="*"
)
@mixin_appmetrica_log(dp)
@mixin_can_repeat(dp)
@mixin_state
async def handler_end(alice: AliceRequest, state: State = None, true_end: bool = False, **kwargs):
    logging.info(f"User: {alice.session.user_id}: Handler->Заключение")

    if true_end:
        text = "Поздравляем, ты отгадали все страны, где мы побывали 🎉"
    else:
        text = "Понимаю, что у тебя свои дела и обязанности, и я ценю всю помощь, что ты уже мне предоставил.\n" \
               "Не переживай, я продолжу мое увлекательное путешествие и поделюсь новостями, когда ты вернёшься."

    if state.current == GameStates.START:
        return await handler_close_game(alice, text=text)

    user = await repositories.UserRepository.get(alice.session.user_id)
    score = user.score
    global_score = await repositories.UserRepository.increase_global_score(user)
    rank = await repositories.UserRepository.get_rank(user)

    text += f"\nЗа игру вы заработали {score} очков." \
            f"\nОбщее количество очков: {global_score}." \
            f"\nВы занимаете {rank} место в рейтинге. Желаете начать заново?"

    state.clear_after_question()
    await dp.storage.set_state(
        alice.session.user_id,
        GameStates.END,
        alice_state=state
    )

    return alice.response(
        text, buttons=NEW_OR_CLOSE_GAME_BUTTONS_GROUP,
        session_state=state.session.model_dump()
    )


# Обработчик повторения последней команды
@dp.request_handler(
    filters.RepeatFilter(),
    state="*"
)
@mixin_appmetrica_log(dp)
@mixin_state
async def handler_repeat(alice: AliceRequest, state: State):
    data = await dp.storage.get_data(alice.session.user_id)

    if state.current == GameStates.GUESS_ANSWER and nlu.calculate_coincidence(
            input_tokens=nlu.lemmatize(nlu.tokenizer(alice.request.command)),
            source_tokens=nlu.lemmatize(["вопрос"])
    ) >= 1.0:
        logging.info(f"User: {alice.session.user_id}: Handler->Повторить->Вопрос")
        if response := data.get(RepeatKey.QUESTION.value, None):
            return response

    if (state.current == GameStates.SELECT_CARD
            and (state.session.need_repeat or nlu.calculate_coincidence(
                input_tokens=nlu.lemmatize(nlu.tokenizer(alice.request.command)),
                source_tokens=nlu.lemmatize(["карточки", "карты"])
            ) >= 0.5)):
        state.session.need_repeat = False
        logging.info(f"User: {alice.session.user_id}: Handler->Повторить->Карточки")
        if response := data.get(RepeatKey.CARDS.value, None):
            return response

    logging.info(f"User: {alice.session.user_id}: Handler->Повторить->Последний ответ")
    response_data = data.get("last", alice.response("Мне нечего повторять"))
    if not isinstance(response_data, dict):
        response = response_data
        return response

    response = AliceResponse(
        response=response_data.get("response"),
        session=response_data.get("session"),
        session_state=response_data.get("session_state"),
        user_state_update=response_data.get("user_state_update"),
        application_state=response_data.get("application_state"),
        version=response_data.get("version")
    )
    return response


@dp.request_handler(filters.CanDoFilter(), state="*")
@mixin_appmetrica_log(dp)
@mixin_can_repeat(dp)
@mixin_state
async def handler_can_do(alice: AliceRequest, state: State, **kwargs):
    logging.info(f"User: {alice.session.user_id}: Handler->Что ты умеешь")
    answer = "Навык 'Отгадай страну с дедушкой' отправит тебя в увлекательное путешествие по всему миру.\n" \
             "Продвигаясь все дальше ты будешь отвечать на вопросы и зарабатывать баллы.\n" \
             "Узнай интересные факты, побывай в красивых местах и проникнись атмосферой " \
             "других стран вместе с дедушкой путешественником."

    buttons = []
    match state.current:
        case GameStates.SELECT_CARD:
            buttons.extend(REPEAT_OR_CLOSE_BUTTONS_GROUP)

        case GameStates.END:
            buttons.extend(NEW_OR_CLOSE_GAME_BUTTONS_GROUP)

        case GameStates.FACT:
            buttons.extend(CONFIRM_BUTTONS_GROUP)

        case GameStates.SHOW_CARDS:
            buttons.extend(CONFIRM_BUTTONS_GROUP)

        case _:
            buttons.extend(MENU_BUTTONS_GROUP)

    return alice.response(
        answer,
        buttons=buttons
    )


@dp.request_handler(filters.HelpFilter(), state="*")
@mixin_appmetrica_log(dp)
@mixin_can_repeat(dp)
@mixin_state
async def handler_help(alice: AliceRequest, state: State, **kwargs):
    logging.info(f"User: {alice.session.user_id}: Handler->Помощь")
    answer = "В данный момент вам доступны следующие команды:\n"
    buttons = []

    match state.current:
        case GameStates.GUESS_ANSWER:
            answer += "Подсказка\n" \
                      "Следующий вопрос\n" \
                      "Повтори\n" \
                      "Повтори вопрос\n" \
                      "Завершить игру"
            buttons.extend(GAME_BUTTONS_GROUP)

        case GameStates.SELECT_CARD:
            answer += "Выбор карточек по наименованию или по номеру\n" \
                      "Повторить карточки\n" \
                      "Завершить игру"
            buttons.extend(REPEAT_OR_CLOSE_BUTTONS_GROUP)

        case GameStates.END:
            answer += "Начать заново\n" \
                      "Завершить игру"
            buttons.extend(NEW_OR_CLOSE_GAME_BUTTONS_GROUP)

        case GameStates.FACT:
            answer += "Согласиться или отказаться от интересного факта"
            buttons.extend(CONFIRM_BUTTONS_GROUP)

        case GameStates.SHOW_CARDS:
            answer += "Продолжить или завершить игру"
            buttons.extend(CONFIRM_BUTTONS_GROUP)

        case _:
            answer += "Начать игру\n" \
                      "Что-ты умеешь\n" \
                      "Повтори\n" \
                      "Завершить игру"
            buttons.extend(MENU_BUTTONS_GROUP)

    return alice.response(answer, buttons=buttons)


@dp.request_handler(filters.RestartFilter(), state="*")
@mixin_appmetrica_log(dp)
async def handler_restart(alice: AliceRequest, **kwargs):
    return await handler_start(alice)


@dp.request_handler(
    filters.OneOfFilter(
        filters.SessionState(GameStates.START),
        filters.SessionState(GameStates.SHOW_CARDS),
    ),
    filters.RejectFilter(),
    state="*"
)
@mixin_appmetrica_log(dp)
@mixin_can_repeat(dp)
@mixin_state
async def handler_reject_game(alice: AliceRequest, state: State, **kwargs):
    return await handler_end(alice, state=state)


@dp.request_handler(
    filters.SessionState(GameStates.START),
    state="*"
)
@mixin_appmetrica_log(dp)
@mixin_can_repeat(dp)
@mixin_state
async def handler_start_game(alice: AliceRequest, state: State, **kwargs):
    logging.info(f"User: {alice.session.user_id}: Handler->Начать игру")
    return await handler_show_cards(alice, state=state)


@dp.request_handler(
    filters.SessionState(GameStates.SHOW_CARDS),
    filters.ConfirmFilter(),
    state="*"
)
@mixin_appmetrica_log(dp)
@mixin_can_repeat(dp, RepeatKey.CARDS)
@mixin_state
async def handler_show_cards(alice: AliceRequest, state: State, **kwargs):
    await dp.storage.set_state(
        alice.session.user_id,
        GameStates.SELECT_CARD,
        alice_state=state
    )

    user = await repositories.UserRepository.get(alice.session.user_id)
    cards: list[Image] = await repositories.CardRepository.get(user)

    if not cards:
        await repositories.UserRepository.clear_passed_cards(user)
        return await handler_end(alice, state=state, true_end=True)

    interface = "screen" if alice.meta.interfaces._raw_kwargs.get("screen", False) == {} else "no_screen"
    answer: schemes.Text = SHOW_CARDS_ANSWER[interface]
    tts = "\n".join([
        answer.tts,
        *[card.title for card in cards]
    ])

    return alice.response_items_list(
        text=answer.src,
        header=answer.src,
        items=cards,
        buttons=REPEAT_OR_CLOSE_BUTTONS_GROUP,
        tts=tts
    )


@dp.request_handler(
    filters.SessionState(GameStates.SELECT_CARD),
    state="*"
)
@mixin_appmetrica_log(dp)
@mixin_can_repeat(dp)
@mixin_state
async def handler_select_card(alice: AliceRequest, state: State, **kwargs):
    user = await repositories.UserRepository.get(alice.session.user_id)
    cards = await repositories.CardRepository.get(user)
    answers = repositories.CardRepository.calculate_answers_with_index(cards)

    result = check_user_answer(alice, [
        SelectCardHandler(answers)
    ])

    if result is None or len(result) == 0:
        return await handler_all(alice, state=state)

    if isinstance(result, list):
        answer: Diff = result[0]
        state.session.selected_card = models.CardType(answer.answer)
    else:
        state.session.selected_card = result

    return await handler_question(alice, state=state)


# @dp.request_handler(
#     filters.SessionState(GameStates.QUESTION_TIME),  # NEVER REACH
#     state="*"
# )
@mixin_appmetrica_log(dp)
@mixin_can_repeat(dp, RepeatKey.QUESTION)
@mixin_state
async def handler_question(alice: AliceRequest, state: State, **kwargs):
    state.clear_after_question()

    selected_card = state.session.selected_card
    user = await repositories.UserRepository.get(alice.session.user_id)
    passed_cards = await repositories.UserRepository.get_passed_cards(
        user, selected_card
    )
    country = await repositories.CountryRepository.random(
        card_type=selected_card,
        passed_cards=passed_cards
    )

    if country is None:
        return await handler_show_cards(
            alice, state=state, extra_text="Вопросы этого типа закончились"
        )
    card = country.card

    await repositories.UserRepository.add_passed_country_card(
        user, country_id=country.id, card_type=selected_card
    )

    print(f"Country: {country.alternatives}")
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
        description=card.question.src,
        buttons=GAME_BUTTONS_GROUP
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
    filters.DontKnowFilter(),
    filters.SessionState(GameStates.GUESS_ANSWER),
    state="*"
)
@mixin_appmetrica_log(dp)
@mixin_can_repeat(dp)
@mixin_state
async def handler_dont_know_answer(alice: AliceRequest, state: State, **kwargs):
    state.session.need_hint = True
    text = choice(DONT_KNOW)
    return alice.response(
        text.src,
        tts=text.tts,
        buttons=GAME_BUTTONS_GROUP
    )


@dp.request_handler(
    filters.TextContainFilter(["подсказка"]),
    filters.SessionState(GameStates.GUESS_ANSWER),
    state="*"
)
@mixin_appmetrica_log(dp)
@mixin_can_repeat(dp, RepeatKey.HINT)
@mixin_state
async def handler_hint(alice: AliceRequest, state: State, **kwargs):
    country_id = state.session.current_question

    country: models.CountryHints = await repositories.CountryRepository.get_hints(
        country_id=country_id
    )

    hints: list[schemes.AnswerWithIndex] = [
        schemes.AnswerWithIndex(index=index, text=hint)
        for index, hint in enumerate(country.hints, 1)
    ]

    hint = None
    for _hint in hints:
        if _hint.index in state.session.latest_hints:
            continue

        hint = _hint
        state.session.latest_hints.append(hint.index)
        break

    if hint is None:
        answer = choice(ALL_HINTS_IS_TAKES)
        text = "\n".join([
            answer.src, *[hint.text.src for hint in hints]
        ])
        tts = "\n".join([
            answer.tts, *[hint.text.tts for hint in hints]
        ])
        return alice.response(
            text,
            tts=tts,
            buttons=GAME_BUTTONS_GROUP
        )

    return alice.response(
        hint.text.src,
        tts=hint.text.tts,
        buttons=GAME_BUTTONS_GROUP
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
        return await handler_end(alice, state=state)

    print(f"{country=}")
    possible_answers = [schemes.AnswerWithIndex(index=0, text=name) for name in country.alternatives]

    result = check_user_answer(alice, handlers=[QuessAnswerHandler(
        answers=possible_answers
    )])

    if result is None:
        if state.session.need_hint:
            # Когда пользователь соглашается на подсказку после неверного ответа
            if filters.ConfirmFilter().check(alice):
                state.session.need_hint = False
                return await handler_hint(alice, state=state)

            # Когда пользователь не соглашается на подсказку после неверного ответа
            elif filters.RejectFilter().check(alice):
                state.session.need_hint = False
                answer: schemes.Text = choice(HINT_DONT_NEED)
                return alice.response(
                    answer.src,
                    tts=answer.tts
                )

        elif filters.TextContainFilter(["нет"]).check(alice):
            return await handler_dont_know_answer(alice, state=state)

        return await handler_false_answer(alice, state=state)

    first_country: Diff = result[0]
    if first_country.coincidence >= 0.5:
        return await handler_true_answer(alice, state=state)

    return await handler_show_cards(alice, state=state)


@mixin_appmetrica_log(dp)
@mixin_can_repeat(dp)
@mixin_state
async def handler_true_answer(alice: AliceRequest, state: State, **kwargs):
    country_id = state.session.current_question
    selected_card = state.session.selected_card
    try_count = state.session.try_count
    latest_hints = state.session.latest_hints

    user = await repositories.UserRepository.get(
        alice.session.user_id
    )
    await repositories.UserRepository.increase_score(
        user, 5 - try_count - bool(latest_hints)
    )
    country: models.CountryShortView = await repositories.CountryRepository.get_card_with_names(
        country_id=country_id,
        card_type=selected_card
    )
    card: models.Card = country.card
    answer = card.answers.correct

    await dp.storage.set_state(
        alice.session.user_id,
        GameStates.FACT,
        alice_state=state
    )

    return alice.response(
        answer.src,
        tts=answer.tts,
        buttons=CONFIRM_BUTTONS_GROUP
    )


@mixin_appmetrica_log(dp)
@mixin_can_repeat(dp)
@mixin_state
async def handler_false_answer(alice: AliceRequest, state: State, **kwargs):
    country_id = state.session.current_question
    selected_card = state.session.selected_card

    country: models.CountryShortView = await repositories.CountryRepository.get_card_with_names(
        country_id=country_id,
        card_type=selected_card
    )
    card: models.Card = country.card
    answer = card.answers.incorrect

    state.session.try_count += 1
    state.session.need_hint = True

    if state.session.try_count >= 3:
        await dp.storage.set_state(
            alice.session.user_id,
            GameStates.FACT,
            alice_state=state
        )
        # TODO: Тут должен быть answer.incorrect
        answer = choice(INCORRECT_ANSWERS)
        country_text = INCORRECT_ANSWERS_COUNTRY[country.name]
        return alice.response(
            "\n".join([country_text.src, answer.src]),
            tts="\n".join([country_text.tts, answer.tts]),
            buttons=CONFIRM_BUTTONS_GROUP
        )

    # TODO: А тут INCORRECT_ANSWERS

    return alice.response(
        answer.src,
        tts=answer.tts,
        buttons=GAME_BUTTONS_GROUP
    )


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
        state=GameStates.SHOW_CARDS,
        alice_state=state
    )

    fact: schemes.Text = choice(country.facts)
    return alice.response(
        fact.src + "\n Хочешь продолжить ?",
        tts=fact.tts + "\n Хочешь продолжить ?",
        buttons=CONFIRM_BUTTONS_GROUP
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


@dp.request_handler(state="*")
@mixin_appmetrica_log(dp)
@mixin_state
async def handler_all(alice: AliceRequest, state: State):
    logging.info(f"User: {alice.session.user_id}: Handler->Общий обработчик")
    interface = "screen" if alice.meta.interfaces._raw_kwargs.get("screen", False) == {} else "no_screen"

    answer: schemes.Text
    buttons = []
    match state.current:
        case GameStates.SELECT_CARD:
            state.session.need_repeat = True
            answers = SELECT_CARD_ANYTHING_ELSE_MOMENT[interface]
            answer = choice(answers)
            buttons.extend(REPEAT_OR_CLOSE_BUTTONS_GROUP)

        case GameStates.END:
            answer = choice(END_ANYTHING_ELSE_MOMENT)
            buttons.extend(NEW_OR_CLOSE_GAME_BUTTONS_GROUP)

        case GameStates.FACT:
            answer = choice(FACT_ANYTHING_ELSE_MOMENT)
            buttons.extend(CONFIRM_BUTTONS_GROUP)

        case GameStates.SHOW_CARDS:
            answer = choice(CONTINUE_ANYTHING_ELSE_MOMENT)
            buttons.extend(CONFIRM_BUTTONS_GROUP)

        case _:
            answer = choice(REPEAT_PLEASE)
            buttons.extend(MENU_BUTTONS_GROUP)

    return alice.response(
        answer.src,
        tts=answer.tts,
        buttons=buttons
    )


@dp.errors_handler()
@mixin_appmetrica_log(dp)
async def the_only_errors_handler(alice, e):
    logging.error('An error!', exc_info=e)
    return alice.response('Кажется что-то пошло не так. ')
