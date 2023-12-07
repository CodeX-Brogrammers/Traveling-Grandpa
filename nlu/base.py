from functools import lru_cache
from typing import Union

import pymorphy2

morph = pymorphy2.MorphAnalyzer()


def lemmatize(tokens: list[str]) -> list[str]:
    return [morph.parse(token)[0].normal_form for token in tokens]


def tokenizer(text: str) -> list[str]:
    text = text.lower().replace("-", " ")
    return text.split()


def calculate_coincidence(
        input_tokens: Union[set[str], list[str]],
        source_tokens: Union[set[str], list[str]]) -> float:
    """
    Эта функция предназначена для вычисления коэффициента совпадения между двумя наборами токенов.
    Она принимает два набора токенов (input_tokens и source_tokens)
    и возвращает число от 0.0 до 1.0, обозначающее коэффициент совпадения.
    """
    if isinstance(input_tokens, list):
        input_tokens = set(input_tokens)
    if isinstance(source_tokens, list):
        source_tokens = set(source_tokens)
    try:
        return len(input_tokens & source_tokens) / len(source_tokens)
    except ZeroDivisionError:
        return 0.0


def find_occurrences(words: list[str], find_words: list[str], skip_index: set[int] = None) -> set:
    if skip_index is None:
        skip_index = set()
    result = set()
    last_index = -1
    for i, word in enumerate(words):
        if word in find_words and not skip_index.intersection((i,)):
            if last_index == -1:
                last_index = i
                result.add(i)
                continue

            if last_index != -1 and last_index == i - 1:
                result.add(i)
    return result


def exclude_words(words: list[str], enters: set[int]) -> bool:
    for number in enters:
        if number >= 1 and number != len(words):
            if words[number - 1] in ("не", "ни"):
                break
    else:
        return False
    return True


def find_common_words(tokens: list[str]) -> set[str]:
    tokens = [set(lemmatize(tokenizer(token))) for token in tokens]
    result = set()
    tokens_len = len(tokens)
    for i in range(tokens_len):
        if (i - 1 >= 0) or (i + 1 <= tokens_len - 1):
            [
                result.add(
                    value
                ) for value in tokens[i].intersection(tokens[i - 1])
            ]
    return result


def remove_common_words(text_tokens: list[str], words: set[str]) -> list[str]:
    result = [word for word in text_tokens if word not in words]
    return result


@lru_cache()
def declension_of_word_after_numeral(word: str, number: int) -> str:
    """
    Данный метод предназначен для склонения слова после числительного в соответствии с числом.
    Он принимает на вход строку word (слово, которое требуется склонять)
    и целочисленное значение number (число, по которому производится склонение)
    """
    word = morph.parse(word)[0]
    return word.make_agree_with_number(number).word

