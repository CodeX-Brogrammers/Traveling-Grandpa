from aioalice.types import Button

from schemes import Text

OK_BUTTON = Button('Да')
REJECT_BUTTON = Button('Нет')
REPEAT_BUTTON = Button('Повтори')
GO_BUTTON = Button("Поехали")
GO_BUTTON_MENU = Button("Поехали", hide=False)
REPEAT_QUESTION_BUTTON = Button("Повторить вопрос")
YOU_CAN_BUTTON = Button('Что ты умеешь ?')
YOU_CAN_BUTTON_MENU = Button('Что ты умеешь ?', hide=False)
HELP_BUTTON = Button('Помощь')
HELP_BUTTON_MENU = Button("Помощь", hide=False)
HINT_BUTTON = Button('Подсказка')
NEXT_BUTTON = Button('Следующий вопрос')
NEW_GAME_BUTTON_MENU = Button('Новая игра', hide=False)
CLOSE_BUTTON = Button('Выход')
CLOSE_BUTTON_MENU = Button('Выход', hide=False)

MENU_BUTTONS_GROUP = [
    GO_BUTTON_MENU,
    HELP_BUTTON_MENU,
    YOU_CAN_BUTTON_MENU,
    CLOSE_BUTTON_MENU,
]
GAME_BUTTONS_GROUP = [HINT_BUTTON, NEXT_BUTTON, HELP_BUTTON, CLOSE_BUTTON]
CONFIRM_BUTTONS_GROUP = [OK_BUTTON, REJECT_BUTTON]
NEW_OR_CLOSE_GAME_BUTTONS_GROUP = [NEW_GAME_BUTTON_MENU, CLOSE_BUTTON_MENU]
REPEAT_OR_CLOSE_BUTTONS_GROUP = [REPEAT_BUTTON, CLOSE_BUTTON]

POSSIBLE_ANSWER = ("Начинаем ?", "Готовы начать ?", "Поехали ?")
CONTINUE_ANSWER = ("Продолжим ?", "Едем дальше ?")
FACT_ANSWER = ("Хотите послушать интересный факт ?",)


INCORRECT_ANSWERS = (
    Text(
        src="Мы не смогли угадать страну, но можем узнать её название и интересный факт, ты согласен?",
        tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/3f261d74-11fd-4ee7-b8dc-743d2adbcbb8.opus'>"
    ),
    Text(
        src="Эх, ты не угадал. Но ничего страшного, давай послушаем интересный факт про эту страну и узнаем её название?",
        tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/cd9502cd-b8d1-493f-ac8d-448592f1a564.opus'>"
    ),
    Text(
        src="Неудача! Так и не угадали страну... Но нам повезет в следующий раз, а сейчас давай послушаем интересный факт об этой стране и узнаем как её называют?",
        tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/52dd50dc-fe45-42ba-a743-0b4d48843e9b.opus'>"
    ),
    Text(
        src="Что ж, к сожалению, ты не смог угадать страну, но не расстраивайся! У тебя еще будет шанс с другой страной, а пока, не хочешь узнать немного интересных фактов об этой стране и её название?",
        tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/c9b0a28b-cd0f-4b51-8895-2da585ca66e1.opus'>"
    ),
    Text(
        src="Твои попытки на эту страну закончились! К сожалению нам придётся отправится к следующей стране. Но перед этим, не желаешь послушать интересный факт и название этой страны?",
        tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/b33cf055-ec76-4482-a2f6-85cb5ddc4075.opus'>"
    ),
    Text(
        src="К несчастью, ты так и не смог угадать страну. Но, думаю прежде чем мы отправимся в другое место, тебе будет интересно узнать о некоторых особенностях этой страны и как её называют, не так ли?",
        tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/ca2f5a5d-5ea8-4f81-a27a-743e369a3c1e.opus'>"
    )
)

HINT_DONT_NEED = (
    Text(
        src="Хорошо. Тогда попытаемся отгадать эту страну снова или перейдём к следующему вопросу?",
        tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/e7970315-baee-4345-aad0-7642477a112e.opus'>"
    ),
    Text(
        src="А это смело! Попробуем всё же отгадать эту страну или поедем в следующую?",
        tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/c482a9b9-b941-4539-9a6b-2eb02223e940.opus'>"
    ),
    Text(
        src="Действительно, прибережём подсказку на потом. Отгадываем снова эту страну или едем в следующую?",
        tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/03feef43-80fb-47cf-bc3e-1d0ac6a3dedb.opus'>"
    )
)

DONT_KNOW = (
    Text(
        src="Давай, подумай ещё. Я уверен у нас всё получится. Давай я дам тебе подсказку?",
        tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/3ffee03d-1b9f-4c0e-9561-8aabd5c4880e.opus'>"
    ),
    Text(
        src="Не знаешь? Давай тогда возьмём подсказку?",
        tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/bd57d79a-c1b0-4521-9379-afe57ec68fbb.opus'>"
    ),
    Text(
        src="Ничего страшного! Я думаю мы можем взять подсказку и ты возможно вспомнишь эту страну, берём?",
        tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/be98dfd0-1fbc-45cb-b60b-ed72b88bbe45.opus'>"
    )
)

MAYBE_ERROR = (
    Text(
        src="К сожалению, я не совсем понял, что ты имеешь ввиду. Скажи еще раз.",
        tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/4b91bb06-da11-4035-a0f4-b5e7ae1161fc.opus'>"
    ),
    Text(
        src="Кажется у меня проблемы со связью, я не расслышал что ты сказал. Можешь повторить?",
        tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/9535888a-01d8-4131-a300-a2d2de888515.opus'>"
    ),
    Text(
        src="Прости, но я не расслышал тебя. Пожалуйста, можешь повторить громче?",
        tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/d982e409-f8aa-4b33-9e25-a4f6dadd9326.opus'>"
    )
)