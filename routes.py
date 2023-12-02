from random import choice, shuffle
from typing import Optional
import logging

from aioalice.types import AliceRequest, Button, AliceResponse
from aioalice.dispatcher.storage import MemoryStorage
from beanie import PydanticObjectId
from aioalice import Dispatcher


from mixin import mixin_appmetrica_log, mixin_can_repeat, mixin_state
from state import State, GameStates
from models import RepeatKey
import filters
import models
import nlu


OK_Button = Button('Да')
REJECT_Button = Button('Нет')
REPEAT_Button = Button('Повтори')
REPEAT_QUESTION_Button = Button("Повторить вопрос")
REPEAT_ANSWERS_Button = Button("Повторить ответы")
YOU_CAN_Button = Button('Что ты умеешь ?')
HELP_Button = Button('Помощь')
HINT_Button = Button('Подсказка')
NEXT_Button = Button('Следующий вопрос')
MENU_BUTTONS = [Button("Поехали", hide=False), Button("Помощь", hide=False), Button("Что ты умеешь ?", hide=False)]
GAME_BUTTONS = [HINT_Button, NEXT_Button, HELP_Button]

POSSIBLE_ANSWER = ("Начинаем ?", "Готовы начать ?", "Поехали ?")
CONTINUE_ANSWER = ("Продолжим ?", "Едем дальше ?")
FACT_ANSWER = ("Хотите послушать интересный факт ?",)


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


@dp.request_handler(filters.CanDoFilter(), state="*")
@mixin_appmetrica_log(dp)
@mixin_can_repeat(dp)
@mixin_state
async def handler_can_do(alice: AliceRequest, state: State, **kwargs):
    logging.info(f"User: {alice.session.user_id}: Handler->Что ты умеешь")
    answer = "Навык будет задавать вам вопросы и предлагать варианты ответов. " \
             "Для успешного прохождения навыка вам нужно ответить верно как можно больше раз. " \
             "У вас есть  возможность взять подсказку для вопроса, но количество подсказок ограничено."
    _state = await dp.storage.get_state(alice.session.user_id, state)
    if _state.upper() in ("DEFAULT_STATE", "*"):
        answer = f"{answer}\n{choice(POSSIBLE_ANSWER)}"
    if _state.upper() == "FACT":
        answer = f"{answer}\n{choice(POSSIBLE_ANSWER)}"
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
                 "3. Повтори ответы \n" \
                 "4. Подсказка \n" \
                 "5. Сколько осталось подсказок \n" \
                 "6. Пропустить вопрос - если вопрос сложный, то так уж и быть пропустим его \n" \
                 "7. Перезапуск - начнем с начала \n" \
                 "8. Выход - мы остановим лекцию и вы спокойно сможете идти по своим делам \n"
        return alice.response(
            answer,
            buttons=[
                REPEAT_QUESTION_Button,
                REPEAT_ANSWERS_Button,
                *GAME_BUTTONS
            ]
        )

    # TODO: Заменить базовый текст помощи, он не напоминает помощь
    answer = "Навык \"Удивительная лекция\" отправит вас в увлекательное путешествие. " \
             "Продвигаясь все дальше вы будете отвечать на вопросы и зарабатывать баллы. " \
             "Погрузитесь в атмосферу Древнего Рима, Средневековья," \
             " Эпохи Возрождения вместе с замечательным проводником Авророй Хисторией. "
    if fsm_state.upper() in ("START", "*"):
        answer = f"{answer}\n{choice(POSSIBLE_ANSWER)}"
        return alice.response(answer, buttons=MENU_BUTTONS)
    return alice.response(answer)


def repeat_answers(alice: AliceRequest):
    state = State.from_request(alice)

    answers = state.session.current_answers
    text = " \n".join((
        "Варианты ответов:",
        *[f"{i}: {answer}" for i, answer in answers]
    ))
    tts = " \n".join((
        "Варианты ответов:",
        *[f"{i}-й {answer}" for i, answer in answers]
    ))
    buttons = [
        Button(
            title=text,
            payload={
                "is_true": i == state.session.current_true_answer,
                "number": i,
                "text": text
            },
            hide=False
        )
        for i, text in answers
    ]
    return {"text": text, "tts": tts, "buttons": buttons}


async def repeat_question(alice: AliceRequest):
    state = State.from_request(alice)
    question = await models.Question.get(PydanticObjectId(state.session.current_question))
    question = dict(
        text=question.full_text.src,
        tts=question.full_text.tts,
        image_id=question.image.yandex_id,
        title="",
        description=question.full_text.src
    )
    answers = repeat_answers(alice)
    buttons = [*answers["buttons"], *GAME_BUTTONS]
    question["tts"] += f"\n{answers['tts']}"
    return alice.response_big_image(
        **question,
        buttons=buttons
    )


# Обработчик повторения последней команды
@dp.request_handler(filters.RepeatFilter(), state="*")
@mixin_appmetrica_log(dp)
@mixin_state
async def handler_repeat(alice: AliceRequest, state: State):
    _state = await dp.storage.get_state(alice.session.user_id, state)
    data = await dp.storage.get_data(alice.session.user_id)
    if _state.upper() in ("QUESTION_TIME", "GUESS_ANSWER", "HINT"):
        if nlu.calculate_coincidence(
                input_tokens=nlu.lemmatize(nlu.tokenizer(alice.request.command)),
                source_tokens=nlu.lemmatize(["вопрос"])
        ) >= 1.0:
            if data.get("last_func", "") != handler_fact_confirm.__name__:
                logging.info(f"User: {alice.session.user_id}: Handler->Повторить->Вопрос")
                if response := data.get(RepeatKey.QUESTION, None):
                    return response
                return await repeat_question(alice)

        if nlu.calculate_coincidence(
                input_tokens=nlu.lemmatize(nlu.tokenizer(alice.request.command)),
                source_tokens=nlu.lemmatize(["ответ"])
        ) >= 1.0:
            if data.get("last_func", "") != handler_fact_confirm.__name__:
                logging.info(f"User: {alice.session.user_id}: Handler->Повторить->Ответы")
                answers = repeat_answers(alice)
                return alice.response(answers["text"], tts=answers["tts"], buttons=answers["buttons"])

    logging.info(f"User: {alice.session.user_id}: Handler->Повторить->Последний ответ")
    response = data.get("last", alice.response("Мне нечего повторять"))
    return response


@dp.request_handler(filters.RestartFilter(), state="*")
@mixin_appmetrica_log(dp)
async def handler_restart(alice: AliceRequest, **kwargs):
    return await handler_start(alice)


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
        text, buttons=[OK_Button, REJECT_Button],
        session_state=state.session.dict()
    )


@dp.request_handler(
    filters.TextContainFilter(["подсказка"]),
    filters.OneOfFilter(
        filters.SessionState(GameStates.QUESTION_TIME),
        filters.SessionState(GameStates.GUESS_ANSWER),
        filters.SessionState(GameStates.FACT)
    ),
    state="*"
)
@mixin_appmetrica_log(dp)
@mixin_can_repeat(dp, RepeatKey.HINT)
@mixin_state
async def handler_hint(alice: AliceRequest, state: State, **kwargs):
    # Получить ID вопроса из State-а
    # Если у пользователя достаточно баллов, даем подсказку
    # Иначе не даем
    user_tokens = nlu.lemmatize(alice.request.nlu.tokens)
    number_of_hints = state.session.number_of_hints
    if number_of_hints == 0:
        logging.info(f"User: {alice.session.user_id}: Handler->Подсказка->Больше нет подсказок")
        return alice.response(f"У вас уже закончились все подсказки. ")

    fsm_state = await dp.storage.get_state(alice.session.user_id, state)
    if fsm_state.upper() == "FACT":
        return alice.response(
            f"У вас есть ещё {number_of_hints}  "
            f"{nlu.declension_of_word_after_numeral('подсказка', number_of_hints)}. ",
            buttons=[OK_Button, REJECT_Button]
        )
    if "сколько" in user_tokens or "остаться" in user_tokens:
        logging.info(f"User: {alice.session.user_id}: Handler->Подсказка->Сколько осталось")
        buttons = []
        if fsm_state.upper() in ("QUESTION_TIME", "GUESS_ANSWER"):
            buttons = repeat_answers(alice)["buttons"]
        return alice.response(
            f"У вас есть ещё {number_of_hints}  "
            f"{nlu.declension_of_word_after_numeral('подсказка', number_of_hints)}. ",
            buttons=buttons
        )

    if last_response := (await dp.storage.get_data(alice.session.user_id)).get(RepeatKey.HINT, None):
        if isinstance(last_response, AliceResponse):
            if "У вас есть ещё " in last_response.response.text:
                last_response.response.text = last_response.response.text.rsplit("\n", 1)[0]
                return last_response
        else:
            if "У вас есть ещё " in last_response.get("response", {}).get("text", ""):
                last_response["response"]["text"] = last_response["response"]["text"].rsplit("\n", 1)[0]
                return last_response
        return last_response

    logging.info(f"User: {alice.session.user_id}: Handler->Подсказка->Отправка")
    await dp.storage.set_state(
        alice.session.user_id,
        state=GameStates.GUESS_ANSWER,
        alice_state=state
    )
    question_id = state.session.current_question
    question = await models.Question.get(PydanticObjectId(question_id))
    answers = repeat_answers(alice)

    state.session.number_of_hints -= 1
    number_of_hints = state.session.number_of_hints
    if number_of_hints > 0:
        left_hints = f"У вас есть ещё {number_of_hints}  " \
                     f"{nlu.declension_of_word_after_numeral('подсказка', number_of_hints)}. "
    else:
        left_hints = "К сожалению, у вас не осталось больше подсказок. "
    return alice.response(
        " \n".join(("Подсказка: ", question.hint.src, left_hints)),
        tts=" \n".join((
            '<speaker audio="dialogs-upload/97e0871e-cf33-4da5-9146-a8fa353b965e/026b63b2-162e-4d0a-a60a-735b10adb15f.opus">',
            "Подсказка: ", question.hint.tts, left_hints)),
        buttons=[*answers["buttons"], *GAME_BUTTONS]
    )


@dp.request_handler(
    filters.ConfirmFilter(),
    filters.SessionState(GameStates.START),
    state="*"
)
@mixin_appmetrica_log(dp)
@mixin_can_repeat(dp)
async def handler_start_game(alice: AliceRequest, **kwargs):
    logging.info(f"User: {alice.session.user_id}: Handler->Начать игру")
    return await handler_question(alice)


# Отказ от игры и выход
@dp.request_handler(
    filters.RejectFilter(),
    filters.SessionState(GameStates.START),
    state="*"
)
@mixin_appmetrica_log(dp)
async def handler_reject_game(alice: AliceRequest, **kwargs):
    logging.info(f"User: {alice.session.user_id}: Handler->Отмена игры")
    answer = "Было приятно видеть вас на моей лекции. Заходите почаще, всегда рада."
    return alice.response(answer, end_session=True)


@dp.request_handler(
    filters.ConfirmFilter(),
    filters.SessionState(GameStates.QUESTION_TIME),
    state="*"
)
@mixin_appmetrica_log(dp)
@mixin_can_repeat(dp, RepeatKey.QUESTION)
@mixin_state
async def handler_question(alice: AliceRequest, state: State, **kwargs):
    # Получить случайный вопрос
    # |-> Можно сохранять в сессии пройденные вопросы
    # Сохранить его ID в State
    # Отправить вопрос с вариантами ответов
    logging.info(f"User: {alice.session.user_id}: Handler->Получение вопроса")
    state.session.current_question = None
    await dp.storage.set_state(
        alice.session.user_id,
        state=GameStates.GUESS_ANSWER,
        alice_state=state
    )
    user_data = await models.UserData.get_user_data(alice.session.user_id)
    data = await models.Question.aggregate([
        {'$match': {'_id': {'$nin': user_data.passed_questions}}},
        {"$sample": {"size": 1}}
    ]).to_list()

    if len(data) == 0:
        logging.info(f"User: {alice.session.user_id}: Handler->Получение вопроса->вопросы закончились")
        user_data.passed_questions = []
        await user_data.save()
        return await handler_end(alice, state=state)

    question: models.Question = models.Question.parse_obj(data[0])
    await user_data.add_passed_question(question.id)
    state.session.question_passed += 1
    state.session.current_question = str(question.id)

    answers = question.answers
    shuffle(answers)
    answers = [(index, answer) for index, answer in enumerate(answers, 1)]
    text = question.full_text.src
    tts = " \n".join((
        question.full_text.tts, "Варианты ответов:",
        *[f"{i}-й {answer.text.tts}" for i, answer in answers]
    ))

    buttons = [
        Button(
            title=answer.text.src,
            payload={
                "is_true": answer.is_true,
                "number": i,
                "text": answer.text.src
            },
            hide=False
        )
        for i, answer in answers]
    buttons += GAME_BUTTONS
    state.session.current_answers = [(i, answer.text.src) for i, answer in answers]
    state.session.current_true_answer = [i for i, answer in answers if answer.is_true][0]
    state.session.try_number = 0
    return alice.response_big_image(
        text,
        tts=tts,
        buttons=buttons,
        image_id=question.image.yandex_id,
        title="",
        description=text
    )


@dp.request_handler(
    filters.RejectFilter(),
    filters.SessionState(GameStates.QUESTION_TIME),
    state="*"
)
@mixin_appmetrica_log(dp)
@mixin_state
async def handler_reject_question(alice: AliceRequest, state: State, **kwargs):
    return await handler_end(alice, state)


@dp.request_handler(
    filters.OneOfFilter(
        filters.TextContainFilter(["следующий", "вопрос"]),
        filters.TextContainFilter(["пропустить", "вопрос"]),
        filters.NextFilter()
    ),
    filters.SessionState(GameStates.GUESS_ANSWER),
    state="*"
)
@mixin_appmetrica_log(dp)
async def handler_skip_question(alice: AliceRequest):
    return await handler_question(alice)


@dp.request_handler(
    filters.OneOfFilter(
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
    filters.SessionState(GameStates.GUESS_ANSWER),
    state="*"
)
@mixin_can_repeat(dp)
async def handler_quess_answer(alice: AliceRequest):
    result = nlu.check_user_answer(alice)
    if not isinstance(result, models.UserCheck):
        return await handler_answer_brute_force(alice)

    if result.is_true_answer:
        return await handler_true_answer(alice)
    return await handler_false_answer(alice, diff=result.diff)


@mixin_appmetrica_log(dp)
@mixin_state
async def handler_true_answer(alice: AliceRequest, state: State, **kwargs):
    # Получить ID вопроса из State-а
    # Если ответ верный, добавить балл
    logging.info(f"User: {alice.session.user_id}: Handler->Отгадал ответ")
    state.session.score += 1

    await dp.storage.set_state(
        alice.session.user_id,
        state=GameStates.FACT,
        alice_state=state
    )
    session = state.session
    answer_text = session.current_answers[session.current_true_answer - 1][1]
    question = await models.Question.get(PydanticObjectId(session.current_question))
    answer = [answer for answer in question.answers if answer.text.src == answer_text][0]
    fact_text = choice(FACT_ANSWER)
    return alice.response(
        " \n".join((answer.description.src, fact_text)),
        tts=" \n".join((
            '<speaker audio="dialogs-upload/97e0871e-cf33-4da5-9146-a8fa353b965e/5a095b4c-4529-473e-acc4-5bb2e29c8235.opus">',
            answer.description.tts, fact_text
        )),
        buttons=[OK_Button, REJECT_Button]
    )


@mixin_appmetrica_log(dp)
@mixin_state
async def handler_answer_brute_force(alice: AliceRequest, state: State, **kwargs):
    logging.info(f"User: {alice.session.user_id}: Handler->Перебор ответов")
    await dp.storage.set_state(
        alice.session.user_id,
        state=GameStates.GUESS_ANSWER,
        alice_state=state
    )

    answers = repeat_answers(alice)
    additional_text = ["Хорошая попытка, но попробуйте выбрать один из вариантов ответов. ", answers["text"]]
    buttons = answers["buttons"]
    buttons += GAME_BUTTONS
    if state.session.number_of_hints > 0 and state.session.try_number < 1:
        additional_text.append("\nНапоминаю, что вы можете использовать подсказку. ")
        buttons.append(HINT_Button)

    return alice.response(
        " \n".join(additional_text),
        tts=" \n".join((
            '<speaker audio="dialogs-upload/97e0871e-cf33-4da5-9146-a8fa353b965e/17d961b9-64f1-4cbf-9c8b-c0ff959fbb30.opus"> ',
            *additional_text)),
        buttons=buttons
    )


@mixin_appmetrica_log(dp)
@mixin_state
async def handler_false_answer(alice: AliceRequest, diff: Optional[models.Diff], state: State, **kwargs):
    # Получить ID вопроса из State-а
    # Если ответ неверный, предложить подсказку или отказаться
    if not diff:
        return await handler_all(alice)

    await dp.storage.set_state(
        alice.session.user_id,
        state=GameStates.GUESS_ANSWER,
        alice_state=state
    )
    question = await models.Question.get(PydanticObjectId(state.session.current_question))
    answer = [answer for answer in question.answers if answer.text.src == diff.answer][0]

    additional_text = []
    buttons = []
    if state.session.number_of_hints > 0 and state.session.try_number < 1:
        logging.info(f"User: {alice.session.user_id}: Handler->Не отгадал ответ")
        additional_text.append("Попробуйте ещё раз отгадать ответ. ")
        additional_text.append("Напоминаю, что вы можете использовать подсказку. ")
        buttons += GAME_BUTTONS
        buttons += repeat_answers(alice)["buttons"]
    elif state.session.number_of_hints <= 0 and state.session.try_number <= 1:
        additional_text.append("Попробуйте ещё раз отгадать ответ. ")
        buttons += GAME_BUTTONS[1:]
        buttons += repeat_answers(alice)["buttons"]
    else:
        logging.info(f"User: {alice.session.user_id}: Handler->Не отгадал ответ 2 раза")
        await dp.storage.set_state(
            alice.session.user_id,
            state=GameStates.FACT,
            alice_state=state
        )
        true_answer = state.session.current_answers[state.session.current_true_answer - 1]
        additional_text.append(f"Верный ответ был: {true_answer[1]} ")
        additional_text.append(choice(FACT_ANSWER))
        buttons = [OK_Button, REJECT_Button]

    state.session.try_number += 1
    return alice.response(
        " \n".join((answer.description.src, *additional_text)),
        tts=" \n".join((
            '<speaker audio="dialogs-upload/97e0871e-cf33-4da5-9146-a8fa353b965e/17d961b9-64f1-4cbf-9c8b-c0ff959fbb30.opus">',
            answer.description.tts, *additional_text)),
        buttons=buttons
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
    question_id = state.session.current_question
    question = await models.Question.get(PydanticObjectId(question_id))
    state.session.current_question = None
    continue_answer = choice(CONTINUE_ANSWER)
    await dp.storage.set_state(
        alice.session.user_id,
        state=GameStates.QUESTION_TIME,
        alice_state=state
    )
    return alice.response(
        " \n".join((question.fact.src, continue_answer)),
        tts=" \n".join((
            '<speaker audio="dialogs-upload/97e0871e-cf33-4da5-9146-a8fa353b965e/e0d1b286-3083-40c5-b40c-41cd5304f06c.opus">',
            question.fact.tts, continue_answer)),
        buttons=[OK_Button, REJECT_Button]
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
    return await handler_question(alice)


@dp.request_handler(
    filters.ConfirmFilter(),
    filters.SessionState(GameStates.END),
    state="*"
)
@mixin_appmetrica_log(dp)
async def handler_restart_game(alice: AliceRequest, **kwargs):
    logging.info(f"User: {alice.session.user_id}: Handler->Перезапуск игры")
    alice._raw_kwargs["state"]["session"] = {}
    return await handler_question(alice)


@dp.request_handler(
    filters.RejectFilter(),
    filters.SessionState(GameStates.END),
    state="*"
)
@mixin_appmetrica_log(dp)
async def handler_confirm_close_game(alice: AliceRequest, **kwargs):
    logging.info(f"User: {alice.session.user_id}: Handler->Завершение игры")
    text = "До новых встреч 👋"
    return alice.response(
        text,
        '<speaker audio="dialogs-upload/97e0871e-cf33-4da5-9146-a8fa353b965e/c3b98c8b-7dc0-4b19-93be-cf6b5d77fb6b.opus">' + text,
        end_session=True)


@dp.request_handler(state="*")
@mixin_appmetrica_log(dp)
@mixin_state
async def handler_all(alice: AliceRequest, state: State):
    logging.info(f"User: {alice.session.user_id}: Handler->Общий обработчик")
    _state = await dp.storage.get_state(alice.session.user_id, state)
    if _state == GameStates.GUESS_ANSWER:
        text = "Извините, я вас не понимаю, выбирайте из доступных вариантов ответа. \n"
        answers = repeat_answers(alice)
        text += answers["text"]
        return alice.response(text, buttons=[*answers["buttons"], *GAME_BUTTONS])
    elif _state == GameStates.FACT:
        text = "Извините, я вас не понимаю, повторите пожалуйста. Вы даёте согласие или отказываетесь?"
        return alice.response(text, buttons=[OK_Button, REJECT_Button])
    else:
        text = "Извините, я вас не понимаю, повторите пожалуйста. "
    return alice.response(text)


@dp.errors_handler()
@mixin_appmetrica_log(dp)
async def the_only_errors_handler(alice, e):
    logging.error('An error!', exc_info=e)
    return alice.response('Кажется что-то пошло не так. ')
