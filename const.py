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
GAME_BUTTONS_GROUP = [HINT_BUTTON, REPEAT_BUTTON, NEXT_BUTTON, HELP_BUTTON, CLOSE_BUTTON]
CONFIRM_BUTTONS_GROUP = [OK_BUTTON, REJECT_BUTTON]
NEW_OR_CLOSE_GAME_BUTTONS_GROUP = [NEW_GAME_BUTTON_MENU, CLOSE_BUTTON_MENU]
REPEAT_OR_CLOSE_BUTTONS_GROUP = [REPEAT_BUTTON, CLOSE_BUTTON]

POSSIBLE_ANSWER = ("Начинаем ?", "Готовы начать ?", "Поехали ?")
CONTINUE_ANSWER = ("Продолжим ?", "Едем дальше ?")
FACT_ANSWER = ("Хотите послушать интересный факт ?",)

# TODO: Изменить ответы
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

REPEAT_PLEASE = (
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

SELECT_CARD_ANYTHING_ELSE_MOMENT = (
    Text(
        src="Кажется у нас проблемы со связью, какую карточку ты выбрал ?",
        tts=''
    ),
    Text(
        src="Извини, но такой карточки нет, если нужно я могу повторить их.",
        tts=''
    ),
)

END_ANYTHING_ELSE_MOMENT = (
    Text(
        src="Извини, ты хочешь начать новую игру или завершить её ?",
        tts=''
    ),
)

FACT_ANYTHING_ELSE_MOMENT = (
    Text(
        src="Это конечно хорошо, но ты хочешь послушать интересный факт ?",
        tts=''
    ),
)

CONTINUE_ANYTHING_ELSE_MOMENT = (
    Text(
        src="Кажется у нас проблемы со связью, ты хочешь продолжить ?",
        tts=''
    ),
)

ALL_HINTS_IS_TAKES = (
    Text(
        src="Извини, ты получил все подсказки об этой стране. Повторю их ещё раз.",
        tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/d32a9542-d430-4467-89f2-582427a9ab73.opus'>"
    ),
    Text(
        src="К сожалению, ты уже получил все подсказки. Скажу их еще раз.",
        tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/42c8e9e7-85af-42fd-bc51-249641e98b58.opus'>"
    ),
    Text(
        src="К несчастью подсказок больше нет, ты уже получил каждую из них .  Повторю  их ещё раз.",
        tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/118236ae-abb8-453d-87c2-60a125e92340.opus'>"
    )
)

# TODO: Удалить к чертям как только, так сразу 🔪
INCORRECT_ANSWERS_COUNTRY = {
    "Россия": Text(
        src="И так, правильным ответом была Россия!",
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/ba1682da-4ed4-45c7-9fe5-b65486da2f28.opus">'
    ),
    "Китай": Text(
        src="Эх, правильным ответом был Китай!",
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/fb1c933d-76f7-4549-b65a-f211962d209a.opus">'
    ),
    "Швейцария": Text(
        src="Все это время, правильным ответом была Швейцария!",
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/06bceac2-3860-4927-ad9a-c9c831390264.opus">'
    ),
    "Австрия": Text(
        src="И так, верный вариант ответа - Австрия.",
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/74d3ed9d-8acd-4686-a422-2f9c216a99a2.opus">'
    ),
    "Мексика": Text(
        src="А правильным ответом была Мексика!",
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/fced6cd7-42a2-4d88-995a-e52f044901b3.opus">'
    ),
    "Нидерланды": Text(
        src="Как ты не угадал!? это же Нидерланды!",
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/a5f554f5-097e-4ac1-8334-5aa76ab68c54.opus">'
    ),
    "Германия": Text(
        src="Странно что ты не угадал. Все ведь указывало, именно на Германию!",
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/ec41f622-1620-40c4-9390-c7083f42b974.opus">'
    ),
    "Вьетнам": Text(
        src="Это было близко, но верным ответом является Вьетнам!",
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/866ff03f-3200-49fd-a515-fe8fffc3fb49.opus">'
    ),
    "Сингапур": Text(
        src="Что ж, это не так. Правильный ответ - Сингапур!",
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/1a638b85-bb6a-4774-ae30-3ad4d0079feb.opus">'
    ),
    "Индия": Text(
        src="Твой ответ был не совсем верен. Правильный же ответ - Индия!",
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/341d6a5b-92fc-4514-8ae6-8f33eea9ff3e.opus">'
    ),
    "Великобритания": Text(
        src="Думаю пора тебе услышать правильный ответ. Им является Великобритания!",
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/23689276-079b-4d22-92ed-bc74985dfbd5.opus">'
    ),
    "Польша": Text(
        src="Я скажу тебе правильный ответ. Это была Польша!",
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/c10914dc-08db-4b23-a843-36c010e9166b.opus">'
    ),
    "Канада": Text(
        src="И так,  Канада все это время была правильным ответом!",
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/d5a51af2-afef-4f18-a536-58174a69f5f0.opus">'
    ),
    "Соединённые Штаты Америки": Text(
        src="Настало время назвать правильный ответ. И это - США!",
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/654ba426-a745-46f3-a157-e24a30e492c4.opus">'
    ),
    "Испания": Text(
        src="Довольно! Я называю правильный ответ - Испания!",
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/aef18a6c-43b1-45ba-9f9f-6b2cd872901a.opus">'
    ),
    "Япония": Text(
        src="Это была твоя последняя попытка. Правильный ответ - Япония!",
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/c331df28-6dd4-4cc5-bae3-d3b66e82ad24.opus">'
    ),
    "Франция": Text(
        src="И так, верный вариант ответа - Франция.",
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/b3683965-3c6b-4be5-80b9-3696dfdac3b5.opus">'
    ),
    "Грузия": Text(
        src="Как ты не угадал!? это же Грузия!",
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/c4f3e43c-7d0d-4c48-873a-14e8f23ff0ce.opus">'
    ),
    "Новая Зеландия": Text(
        src="Это была твоя последняя попытка. Правильный ответ - Новая Зеландия!",
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/121bcc3a-af3d-43e1-b0c7-807e47bd648b.opus">'
    ),
    "Греция": Text(
        src="Правильный ответ был так близко! Но это - Греция.",
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/eb3806fc-6382-4809-9aca-a1bbefdee6f4.opus">'
    ),
    "Бельгия": Text(
        src="Думаю пора тебе услышать правильный ответ. Им является Бельгия!",
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/7d36ad7b-5d4a-4e14-a9e3-f5c877ad26d1.opus">'
    ),
    "Объединённые Арабские Эмираты": Text(
        src="И так,  Арабские Эмираты все это время были правильным ответом!",
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/d10b3e4b-27f5-4c9f-817f-fab56eedd00e.opus">'
    ),
    "Кипр": Text(
        src="И так, правильным ответом был Кипр!",
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/3a15d82f-eabd-4db2-88b4-6d16eaf973f2.opus">'
    ),
    "Литва": Text(
        src="Твой ответ был не совсем верен. Правильный же ответ - Литва!",
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/262373c6-66cb-423e-ac15-e5150fd395c7.opus">'
    ),
    "Северная Корея": Text(
        src="Я скажу тебе правильный ответ. Это была Северная Корея!",
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/d282e1ae-664f-4374-b0b2-afba5fd33f0f.opus">'
    ),
    "Узбекистан": Text(
        src="Ты был так близко, но нет. Верный ответ - Узбекистан!",
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/ce0ff260-ee2e-4a1b-827f-bed59198985c.opus">'
    ),
    "Южная Корея": Text(
        src="А правильным ответом была Южная Корея!",
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/416e3d90-3981-4439-9eb0-518106a36115.opus">'
    ),
    "Чехия": Text(
        src="И так, верный вариант ответа - Чехия!",
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/f40c75e1-ecf6-4110-8106-6426010c58d6.opus">'
    ),
    "Казахстан": Text(
        src="Что ж, это не так. Правильный ответ - Казахстан!",
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/75348455-502b-45ea-a256-fa693a5bc90e.opus">'
    ),
    "Норвегия": Text(
        src="Настало время назвать правильный ответ. И это - Норвегия!",
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/5076baf8-bfc7-4473-971d-4f68c9a25667.opus">'
    ),
}
