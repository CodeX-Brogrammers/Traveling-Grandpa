from aioalice.types import Button, Image

from schemes import AnswerWithIndex
from models import CardType

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
HINT_COUNT_BUTTON = Button('Сколько подсказок ?')
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
GAME_BUTTONS_GROUP = [HINT_BUTTON, HINT_COUNT_BUTTON, NEXT_BUTTON, HELP_BUTTON, CLOSE_BUTTON]
CONFIRM_BUTTONS_GROUP = [OK_BUTTON, REJECT_BUTTON]
NEW_OR_CLOSE_GAME_BUTTONS_GROUP = [NEW_GAME_BUTTON_MENU, CLOSE_BUTTON_MENU]
REPEAT_OR_CLOSE_BUTTONS_GROUP = [REPEAT_BUTTON, CLOSE_BUTTON]

POSSIBLE_ANSWER = ("Начинаем ?", "Готовы начать ?", "Поехали ?")
CONTINUE_ANSWER = ("Продолжим ?", "Едем дальше ?")
FACT_ANSWER = ("Хотите послушать интересный факт ?",)

# TODO: Сделать генерацию карточек, нужно когда тема заканчивается
SELECT_CARDS = [
    Image(
        image_id="997614/8e4eda6eb11d49980d4d",
        title="Достопримечательности",
        description="Достопримечательности",
        button=Button(
            title="Достопримечательности",
            payload={
                "selected_card": CardType.ATTRACTIONS
            }
        )
    ),
    Image(
        image_id="1540737/f91ca46e2da86edffc96",
        title="Национальные блюда",
        description="Национальные блюда",
        button=Button(
            title="Национальные блюда",
            payload={
                "selected_card": CardType.NATIONAL_DISHES
            }
        )
    ),
    Image(
        image_id="997614/6b6b4fb3948f86b612e8",
        title="Культурные особенности",
        description="Культурные особенности",
        button=Button(
            title="Культурные особенности",
            payload={
                "selected_card": CardType.CULTURAL_FEATURES
            }
        )
    ),
    Image(
        image_id="997614/6af22da7d2ef486a58e8",
        title="Факты о стране",
        description="Факты о стране",
        button=Button(
            title="Факты о стране",
            payload={
                "selected_card": CardType.FACTS
            }
        )
    ),
    Image(
        image_id="1652229/06aa85c89296ea2dd776",
        title="Творчество",
        description="Творчество",
        button=Button(
            title="Творчество",
            payload={
                "selected_card": CardType.CREATIVITY
            }
        )
    )
]

SELECT_CARDS_ANSWERS = [
    AnswerWithIndex(
        index=1,
        text=CardType.ATTRACTIONS.value
    ),
    AnswerWithIndex(
        index=2,
        text=CardType.NATIONAL_DISHES.value
    ),
    AnswerWithIndex(
        index=3,
        text=CardType.CULTURAL_FEATURES.value
    ),
    AnswerWithIndex(
        index=4,
        text=CardType.FACTS.value
    ),
    AnswerWithIndex(
        index=5,
        text=CardType.CREATIVITY.value
    )
]
