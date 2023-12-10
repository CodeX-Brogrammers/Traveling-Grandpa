from aioalice.types import Button

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
