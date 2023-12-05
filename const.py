from aioalice.types import Button, Image

from schemes import AnswerWithIndex
from models import CardType

OK_BUTTON = Button('Да')
REJECT_BUTTON = Button('Нет')
REPEAT_BUTTON = Button('Повтори')
REPEAT_QUESTION_BUTTON = Button("Повторить вопрос")
REPEAT_ANSWERS_BUTTON = Button("Повторить ответы")
YOU_CAN_BUTTON = Button('Что ты умеешь ?')
HELP_BUTTON = Button('Помощь')
HINT_BUTTON = Button('Подсказка')
NEXT_BUTTON = Button('Следующий вопрос')
MENU_BUTTONS = [
    Button("Поехали", hide=False),
    Button("Помощь", hide=False),
    Button("Что ты умеешь ?", hide=False)
]
GAME_BUTTONS = [HINT_BUTTON, NEXT_BUTTON, HELP_BUTTON]

POSSIBLE_ANSWER = ("Начинаем ?", "Готовы начать ?", "Поехали ?")
CONTINUE_ANSWER = ("Продолжим ?", "Едем дальше ?")
FACT_ANSWER = ("Хотите послушать интересный факт ?",)

SELECT_CARDS = [
    Image(
        image_id="997614/d1a030478031816bf0a3",
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
        image_id="997614/ad00f4d8cc80c3c98161",
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
        image_id="213044/f4ef8b8d98ec8553485d",
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
        image_id="997614/4ea20a45e9e095b3c31c",
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
        image_id="213044/c9bf85a9711ae2e6b1ec",
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
