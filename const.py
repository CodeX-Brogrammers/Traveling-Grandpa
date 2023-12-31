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
REVIEW_BUTTON = Button(
    "Оценить и оставить отзыв о игре",
    url="https://dialogs.yandex.ru/store/skills/5faa86a8-otgadaj-stranu-s-dedushko"
)

MENU_BUTTONS_GROUP = [
    GO_BUTTON_MENU,
    HELP_BUTTON_MENU,
    YOU_CAN_BUTTON_MENU,
    CLOSE_BUTTON_MENU,
]
GAME_BUTTONS_GROUP = [HINT_BUTTON, REPEAT_BUTTON, NEXT_BUTTON, HELP_BUTTON, CLOSE_BUTTON]
CONFIRM_BUTTONS_GROUP = [OK_BUTTON, REJECT_BUTTON]
NEW_OR_CLOSE_GAME_BUTTONS_GROUP = [NEW_GAME_BUTTON_MENU, CLOSE_BUTTON_MENU, REVIEW_BUTTON]
REPEAT_OR_CLOSE_BUTTONS_GROUP = [REPEAT_BUTTON, CLOSE_BUTTON]

TRUE_ANSWER_SOUND = "<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/506b8f87-b86f-4e92-ade2-b2a326d1a585.opus'>"
FALSE_ANSWER_SOUND = "<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/5bf4a70a-89c7-4c5f-b901-11a8bc564e15.opus'>"

CONFIRM_EXIT_ANSWER = Text(
    src="Вы уверены, что хотите выйти из навыка?",
    tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/a6ded371-a761-472b-a9cb-6893e54f987a.opus'>"
)

CONTINUE_ANSWER = (
    Text(
        src="Хочешь продолжить игру ?",
        tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/328ccf9c-cb22-4bee-a601-0c70a7ca8a14.opus'>"
    ),
    Text(
        src="Давай продолжим отгадывать страны ?",
        tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/c2dfcfaa-2f87-42e7-8102-3046361a09a1.opus'>"
    ),
    Text(
        src="Продолжим нашу игру?",
        tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/8c7c9b64-478b-4810-b656-fa778c097851.opus'>"
    )
)

HELP_ANSWER = {
    "main": Text(
        src="В данный момент тебе доступны следующие команды:",
        tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/75575914-55e6-4f57-ba8b-ec171386aba7.opus'>"
    ),
    "hint": Text(
        src="Подсказка",
        tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/f84d7adb-e2f0-4a90-8370-c57e8e0f2ae3.opus'>"
    ),
    "next": Text(
        src="Следующий вопрос",
        tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/b59810ca-4496-43b9-bab2-9189926c9c42.opus'>"
    ),
    "repeat": Text(
        src="Повтори",
        tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/9e202b6e-3eb1-4c70-bec6-0b3160f7709f.opus'>"
    ),
    "repeat_question": Text(
        src="Повтори вопрос",
        tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/416475e3-7d73-4716-98e4-5242d236e291.opus'>"
    ),
    "repeat_cards": Text(
        src="Повторить карточки",
        tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/629b1cb5-24b5-43f6-ab94-00b6083124d2.opus'>"
    ),
    "questions": Text(
        src="Выбор карточек по наименованию или по номеру",
        tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/0d2ad9bc-b323-46cd-abdb-f1d90ab261b4.opus'>"
    ),
    "end": Text(
        src="Завершить игру",
        tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/cdd19227-d955-4266-ac0b-1721db72c220.opus'>"
    ),
    "restart": Text(
        src="Начать заново",
        tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/ba9f1aa7-0fcf-4c2b-b80c-7d31eb290a34.opus'>"
    ),
    "start": Text(
        src="Начать игру",
        tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/4ee8bd24-5c72-45e5-a942-778ad1f86622.opus'>"
    ),
    "agree_or_reject_fact": Text(
        src="Согласиться или отказаться от интересного факта",
        tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/912055bd-a87b-4efc-ad18-ceeb898b9778.opus'>"
    ),
    "continue_or_close_game": Text(
        src="Продолжить или завершить игру",
        tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/6f895543-be53-44bd-add7-247790a4039c.opus'>"
    ),
    "what_can_do": Text(
        src="Что ты умеешь",
        tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/3dc722ea-bc7f-46c9-b483-911466bc2b6d.opus'>"
    )
}

START_ANSWER = Text(
    src="\n".join([
        "Приём! Приём! Как слышно? Это твой дедушка! Я, как всегда, отправился в удивительное путешествие... Но в этот раз мне нужна твоя помощь! Видишь, из-за моих бесконечных приключений я совсем забыл, как называются разные страны. Можешь ли ты мне помочь их отгадать по разным особенностям?\n",
        """Если ты захочешь узнать больше о нашем задании, спроси "Что ты умеешь ?" Если ты что-то забудешь или не поймешь, что делать, то cкажи "Помощь", я дам совет. Возможно у тебя появится что-то важное и тебе нужно будет остановить нашу беседу, просто скажи "Выход" - я всегда пойму.\n""",
        """Но вот главный вопрос: поможешь ли ты мне отгадывать страны? Если ты готов отправиться в это увлекательное путешествие, ответь, пожалуйста, "да".\n""",
        "С любовью, твой дедушка ♥"
    ]),
    tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/6c5352bf-11ac-422c-ab34-316cf9ab5703.opus'>"  # ВКЛ Рация
        "<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/a8f5c513-ec2b-4349-9777-477f0adb86fc.opus'>"  # Звуки Рация
        "<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/eaa6b706-93b4-4fed-a520-1f4278b04674.opus'>"  #
        "<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/6fe073a9-6c6a-4733-8ac6-5474e6799876.opus'>"  #
        "<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/875e4355-8bb7-4091-95b4-83c117aca343.opus'>"  #
        "<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/7a01c488-39bc-44ee-93db-ca4a0524fa8c.opus'>"  # With ♥
)

CLOSE_GAME_ANSWER = Text(
    src="Буду скучать, возвращайся! С любовью, твой дедушка ♥",
    tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/6089b6bc-2b82-4937-9529-64b8fdc4c58e.opus'>"
        "<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/7a01c488-39bc-44ee-93db-ca4a0524fa8c.opus'>"
)

INCORRECT_ANSWERS = (
    Text(
        src='К сожалению, это не правильный ответ. Может быть, стоит воспользоваться подсказкой?',
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/37f7cabc-3add-4f63-a6ae-30899ddf2184.opus">'
    ),
    Text(
        src='Нет, это не верно. Но я могу тебе подсказать, примешь мою помощь?',
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/3a6dced3-ac3b-4cc6-8cfb-38edaadb5cb3.opus">'
    ),
    Text(
        src='Это неправильный ответ. Давай возьмём подсказку?',
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/73b06819-daf4-415e-b8f5-3d285b27e654.opus">'
    ),
    Text(
        src='Не совсем. Хочешь воспользоваться подсказкой?',
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/01748ba6-5d88-4b77-8e5d-74b495c40c35.opus">'
    ),
    Text(
        src='Это неправильно. Но думаю если мы возьмём подсказку, то всё получится. Берём?',
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/d83d71b4-068d-422f-bc97-7dc29dc130d3.opus">'
    ),
    Text(
        src='К сожалению, это неверно. Попробуй еще раз. Я могу предложить тебе подсказку, хочешь ею воспользоваться?',
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/4e211cfe-5ec5-46da-b11a-2808fb6885c3.opus">'
    ),
    Text(
        src='К сожалению, это неверно. Давай попробуем взять подсказку?',
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/b59563e3-cbb4-4653-85ab-f7ba10f3bbaf.opus">'
    ),
    Text(
        src='Это неправильный ответ, мне жаль. Хочешь попробовать ответить снова, взяв подсказку?',
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/80cabdec-0b6f-4ae4-b892-a44c71a326c9.opus">'
    ),
    Text(
        src='Ошибочка вышла. Но не расстраивайся, попробуй еще раз. Я думаю нужно взять подсказку, согласен?',
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/e1cb4034-aa0c-4e6f-b69f-086eb935d214.opus">'
    ),
    Text(
        src='Нет, это не верно. Давай я дам тебе подсказку, может так получится отгадать?',
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/0e369fb8-edaa-4731-8234-5fbd0921e296.opus">'
    ),
    Text(
        src='К сожалению, это неверно. Но не расстраивайся, всё еще может получится. Хочешь подсказку?',
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/6985c2d2-9f88-4afe-867f-0bb25adf1bcc.opus">'
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
SHOW_CARDS_ANSWER = {
    "screen": Text(
        src="Выбери карточку с помощью которой ты будешь угадывать страну",
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/b795e9b2-029d-4feb-ab10-44db891f485f.opus">'
    ),
    "no_screen": Text(
        src="Выбери тему с помощью которой ты будешь угадывать страну",
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/41b4b7f4-71b2-4d72-811f-ad95e57805c5.opus">'
    )
}

SELECT_CARD_ANYTHING_ELSE_MOMENT = {
    "screen": (
        Text(
            src="Кажется у нас проблемы со связью, какую карточку ты выбрал ?",
            tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/13b2198f-741e-4e34-84a9-37777c934a85.opus">'
        ),
        Text(
            src="Извини, но я не понял какую карточку ты выбрал. повтори пожалуйста.",
            tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/53777167-2e16-4744-b842-3fb4327705b6.opus">'
        ),
        Text(
            src="Здесь плохая связь, скажи еще раз какую ты выбрал карточку ?",
            tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/9c4508af-4e85-4676-8cce-02e614b45fb8.opus">'
        ),
    ),
    "no_screen": (
        Text(
            src="Кажется у нас проблемы со связью, какую тему ты выбрал ?",
            tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/6eec85a4-06c6-4adc-9a18-cdea0aea802f.opus">'
        ),
        Text(
            src="Извини, но я не понял какую тему ты выбрал. повтори пожалуйста.",
            tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/9caaa401-01ca-43b2-8ba8-ed3f45c8576e.opus">'
        ),
        Text(
            src="Здесь плохая связь, скажи еще раз какую ты выбрал тему ?",
            tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/f6258b86-0d60-4bf3-b623-97310d5fa586.opus">'
        ),
    )
}

END_ANYTHING_ELSE_MOMENT = (
    Text(
        src="Извини, ты хочешь начать новую игру или завершить её ?",
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/eed5a391-885e-47f6-b920-0d314683c35b.opus">'
    ),
    Text(
        src="Прости, я не понял, ты хочешь начать новую игру или завершить её?",
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/13dee306-a35a-4e4e-a875-451c08273724.opus">'
    ),
    Text(
        src="Я запутался, повтори пожалуйста, ты хочешь начать новую игру или завершить её ?",
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/daa0673a-8337-476e-8d0a-43f6d388564e.opus">'
    ),
)

FACT_ANYTHING_ELSE_MOMENT = (
    Text(
        src="Это конечно хорошо, но ты хочешь послушать интересный факт ?",
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/60285119-4b6b-4ffa-8128-ac7b02fcf3c8.opus">'
    ),
    Text(
        src="Не понял тебя, ты хочешь послушать интересный факт ?",
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/30df4709-16e3-4586-bf7c-f327c15a8fe5.opus">'
    ),
    Text(
        src="Не расслышал тебя, повтори, пожалуйста, хочешь ли ты послушать интересный факт ?",
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/4a76f2a4-d6f1-40ce-b880-9e2f148ec7ff.opus">'
    ),
)

CONTINUE_ANYTHING_ELSE_MOMENT = (
    Text(
        src="Кажется у нас проблемы со связью, ты хочешь продолжить ?",
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/7cf71898-9203-4629-9e72-ad7e2f5901aa.opus">'
    ),
    Text(
        src="Я плохо тебя слышу, ты хочешь продолжить ?",
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/2cef9595-10cf-423c-9ac2-ca323200086d.opus">'
    ),
    Text(
        src="Я не совсем понял тебя, ты хочешь продолжить или нет?",
        tts='<speaker audio="dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/87ee116f-0402-4321-9c5f-4cacdc9fd773.opus">'
    ),
)

CONFIRM_END_ANYTHING_ELSE_MOMENT = (
    Text(
        src="Не совсем понял, что ты говоришь. Ты точно хочешь выйти?",
        tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/25722742-c2e5-4f8c-a6c3-855e4539b7b5.opus'>"
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

ANTI_BRUTE_FORCE_ANSWERS = (
    Text(
        src="Кажется, я слышу названия нескольких стран. Назови, пожалуйста, итоговый ответ.",
        tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/5b9c9e3f-1e91-4cb0-9059-302e756368f7.opus'>"
    ),
    Text(
        src="Хм, может быть, мне послышалось, но кажется ты называешь несколько стран? Давай выберем из них одну как ответ.",
        tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/46188b61-6f5b-418b-877e-25611bdcde98.opus'>"
    ),
    Text(
        src="Сразу несколько ответов я не могу принять. Выбери только одну страну.",
        tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/99380479-f6b3-4fbc-8d93-4f15b080ba32.opus'>"
    )
)

ERROR_ANSWERS = (
    Text(
        src="Ой, что-то связь барахлит. Видимо, далеко я забрался, где сигнал плохо доходит. Не мог бы ты сказать своё последнее предложение ещё раз?",
        tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/25377c8f-775a-4caf-a228-f1eb40a3f708.opus'>"
    ),
    Text(
        src="Представляешь, моя рация опять шипит. Я не смог разобрать твои последние слова, повтори, пожалуйста, что ты сказал.",
        tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/21c88c35-e78d-4b31-9476-98f3d8fc8a7f.opus'>"
    ),
    Text(
        src="Извини, у меня плохой сигнал и я тебя плохо слышу. Пожалуйста, повтори своё последнее предложение.",
        tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/5835b488-740b-4bd1-b34a-655b8baa91e3.opus'>"
    )
)

TRUE_END_ANSWER = Text(
    src="Поздравляю тебя! На этом мои вопросы закончились! "
        "Мы побывали с тобой в удивительных странах, узнали много нового и проверили старые знания. "
        "Отведали необычные национальные блюда, смотрели на уникальные произведения искусства и много того, "
        "что я никогда не забуду! Спасибо за столь увлекательное путешествие и твою помощь!",
    tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/2a05175a-8040-46ad-a932-e052b0d2ba7e.opus'>"
)

END_ANSWER = Text(
    src="Понимаю, что у тебя свои дела и обязанности, я очень ценю всю предоставленную мне помощь.\n"
        "Не переживай, я продолжу мое увлекательное путешествие и поделюсь новостями, когда ты вернёшься.",
    tts="<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/f403dbab-44ca-45e1-a276-a5a74cfcbc25.opus'>sil <[150]>"
        "<speaker audio='dialogs-upload/69d87e76-1810-408c-8de1-4951ad218fa6/8589bcdf-9ac9-4282-9215-7473cd1cfbdd.opus'>"
)
