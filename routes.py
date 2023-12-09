from random import choice
import logging

from aioalice.dispatcher.storage import MemoryStorage
from aioalice.types import AliceRequest
from aioalice import Dispatcher

from nlu.cases import check_user_answer, SelectCardHandler, QuessAnswerHandler
from mixin import mixin_appmetrica_log, mixin_can_repeat, mixin_state
from state import State, GameStates
from schemes import RepeatKey, Diff
from const import (
    MENU_BUTTONS_GROUP,
    GAME_BUTTONS_GROUP,
    SELECT_CARDS,
    SELECT_CARDS_ANSWERS,
    CONFIRM_BUTTONS_GROUP,
    NEW_OR_CLOSE_GAME_BUTTONS_GROUP,
    REPEAT_OR_CLOSE_BUTTONS_GROUP
)
import repositories
import filters
import schemes
import models
import nlu


class HybridStorage(MemoryStorage):
    async def get_state(self, user_id, state: State = None):
        if state is None:
            return super().get_state(user_id)
        return state.current

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

    # TODO: TTS
    # TODO: Картинка для старта
    answer = "Приём, приём... Как слышно? Это твой дедушка!\n" \
             "Я, как всегда, отправился в удивительное путешествие...\n" \
             "Но в этот раз мне нужна твоя помощь!\n" \
             "Видишь, из-за моих бесконечных приключений я совсем забыл, как называются разные страны.\n" \
             "Можешь ли ты мне помочь их отгадать по интересным фактам?\n"

    return alice.response_big_image(
        answer,
        # tts=answer + '<speaker audio="dialogs-upload/97e0871e-cf33-4da5-9146-a8fa353b965e/9484707f-a9ae-4a1c-b8da-8111e026a9a8.opus">',
        image_id="213044/8caa36129ca6356f8981",
        buttons=MENU_BUTTONS_GROUP,
        title="",
        description=answer
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
    close_text = "Буду скучать, возвращайся! С любовью, твой дедушка."
    if text:
        close_text = text + close_text

    return alice.response(
        close_text,
        end_session=True
    )


@dp.request_handler(filters.EndFilter(), state="*")
@mixin_can_repeat(dp)
@mixin_appmetrica_log(dp)
@mixin_state
async def handler_end(alice: AliceRequest, state: State = None, **kwargs):
    logging.info(f"User: {alice.session.user_id}: Handler->Заключение")
    text = "Понимаю, что у тебя свои дела и обязанности, и я ценю всю помощь, что ты уже мне предоставил.\n" \
           "Не переживай, я продолжу мое увлекательное путешествие и поделюсь новостями, когда ты вернёшься.\n" \
           "\n"

    if state.current == GameStates.START:
        return await handler_close_game(alice, text=text)

    user = await repositories.UserRepository.get(alice.session.user_id)
    score = user.score
    global_score = await repositories.UserRepository.increase_global_score(user)
    rank = await repositories.UserRepository.get_rank(user)

    text += f"За игру вы заработали {score} очков.\n" \
            f"Общее количество очков: {global_score}.\n" \
            f"Вы занимаете {rank} место в рейтинге. Желаете начать заново?"

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
@dp.request_handler(filters.RepeatFilter(), state="*")
@mixin_appmetrica_log(dp)
@mixin_state
async def handler_repeat(alice: AliceRequest, state: State):
    # TODO: Сделать повторение
    return alice.response("Повторять нечего")


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
    # TODO: tts
    return alice.response(
        answer,
        buttons=MENU_BUTTONS_GROUP
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
        case GameStates.GUESS_ANSWER | GameStates.FACT | GameStates.QUESTION_TIME:
            answer += "Подсказка\n" \
                      "Сколько осталось подсказок ?\n" \
                      "Следующий вопрос\n" \
                      "Повтори\n" \
                      "Завершить игру"
            buttons.extend(GAME_BUTTONS_GROUP)

        case GameStates.SELECT_CARD:
            answer += "1 по 5. Выбор карточек\n" \
                      "Повторить карточки\n" \
                      "Выход\n"
            buttons.extend(REPEAT_OR_CLOSE_BUTTONS_GROUP)

        case GameStates.END:
            answer += "Начать заново\n" \
                      "Завершить игру"
            buttons.extend(NEW_OR_CLOSE_GAME_BUTTONS_GROUP)

        case _:
            answer += "1. Начать игру\n" \
                      "2. Что-ты умеешь\n" \
                      "3. Повтори\n" \
                      "4. Завершить игру"
            buttons.extend(MENU_BUTTONS_GROUP)

    return alice.response(answer, buttons=buttons)


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

    # TODO: Переделать картинки для карточек
    return alice.response_items_list(
        text=extra_text if extra_text else "Выберите одну из карт",
        header="Выберите одну из карт",
        items=SELECT_CARDS,
        buttons=REPEAT_OR_CLOSE_BUTTONS_GROUP
    )


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
async def handler_dont_know_answer(alice: AliceRequest):
    text = "Мы многого не знаем, попробуйте взять подсказку или перейдите на следующий вопрос. "
    return alice.response(text, buttons=GAME_BUTTONS_GROUP)


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
    user_tokens = nlu.lemmatize(alice.request.nlu.tokens)
    if state.session.number_of_hints <= 0:
        return alice.response(
            "Извини внучок, у тебя больше нет подсказок",
            buttons=GAME_BUTTONS_GROUP
        )

    elif any([value in user_tokens for value in ("сколько", "остаться", "количество")]):
        hints_count = state.session.number_of_hints
        hints_count_text = nlu.declension_of_word_after_numeral('подсказка', hints_count)
        return alice.response(
            f"У тебя осталось {hints_count} {hints_count_text}.",
            buttons=GAME_BUTTONS_GROUP
        )

    elif len(state.session.latest_hints) >= 3:
        # TODO: Повторение подсказок
        return alice.response(
            "Извини внучок, ты получил все подсказки об этой стране.",
            buttons=GAME_BUTTONS_GROUP
        )

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
        return alice.response("Извини внучок, ты получил все подсказки об этой стране")

    state.session.number_of_hints -= 1
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
        pass

    print(f"{country=}")
    possible_answers = [schemes.AnswerWithIndex(index=0, text=name) for name in country.alternatives]

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

    if state.session.try_count >= 3:
        await dp.storage.set_state(
            alice.session.user_id,
            GameStates.FACT,
            alice_state=state
        )
        country_name = country.name
        return alice.response(
            f"Ты не угадал, это был {country_name}. Хочешь послушать интересный факт ?",
            buttons=CONFIRM_BUTTONS_GROUP
        )

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
        state=GameStates.QUESTION_TIME,
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


@dp.errors_handler()
@mixin_appmetrica_log(dp)
async def the_only_errors_handler(alice, e):
    logging.error('An error!', exc_info=e)
    return alice.response('Кажется что-то пошло не так. ')
