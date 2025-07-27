from typing import TypedDict
from kamaaalpy.lists import flat_group_by


class Person(TypedDict):
    name: str
    age: int
    city: str


def test_flat_group_by_with_integers_by_even_odd():
    numbers = [1, 2, 3, 4, 5, 6]

    result = flat_group_by(numbers, lambda x: x % 2 == 0)

    expected = {
        False: 5,  # last odd number
        True: 6,  # last even number
    }
    assert result == expected


def test_flat_group_by_with_strings_by_length():
    words = ["cat", "dog", "elephant", "bee", "butterfly"]

    result = flat_group_by(words, lambda x: len(x))

    expected = {
        3: "bee",  # last 3-letter word
        8: "elephant",  # only 8-letter word
        9: "butterfly",  # only 9-letter word
    }
    assert result == expected


def test_flat_group_by_with_strings_by_first_letter():
    words = ["apple", "banana", "cherry", "apricot", "blueberry"]

    result = flat_group_by(words, lambda x: x[0])

    expected = {
        "a": "apricot",  # last word starting with 'a'
        "b": "blueberry",  # last word starting with 'b'
        "c": "cherry",  # only word starting with 'c'
    }
    assert result == expected


def test_flat_group_by_with_empty_list():
    result = flat_group_by([], lambda x: x)

    assert result == {}


def test_flat_group_by_with_single_item():
    result = flat_group_by([42], lambda x: x > 0)

    expected = {True: 42}
    assert result == expected


def test_flat_group_by_overwrites_duplicate_keys():
    numbers = [1, 2, 3, 4, 5, 6, 7, 8]

    result = flat_group_by(numbers, lambda x: x % 3)

    expected = {
        1: 7,  # 1, 4, 7 -> only 7 remains
        2: 8,  # 2, 5, 8 -> only 8 remains
        0: 6,  # 3, 6 -> only 6 remains
    }
    assert result == expected


def test_flat_group_by_with_dictionaries():
    people: list[Person] = [
        {"name": "Alice", "age": 25, "city": "New York"},
        {"name": "Bob", "age": 30, "city": "London"},
        {"name": "Charlie", "age": 25, "city": "New York"},
        {"name": "Diana", "age": 35, "city": "London"},
    ]

    result = flat_group_by(people, lambda person: person["city"])

    expected: dict[str, dict[str, Person]] = {
        "New York": {"name": "Charlie", "age": 25, "city": "New York"},
        "London": {"name": "Diana", "age": 35, "city": "London"},
    }
    assert result == expected


def test_flat_group_by_with_tuples():
    pairs = [(1, "a"), (2, "b"), (1, "c"), (3, "d"), (2, "e")]

    result = flat_group_by(pairs, lambda pair: pair[0])

    expected = {
        1: (1, "c"),  # (1, 'a') gets overwritten by (1, 'c')
        2: (2, "e"),  # (2, 'b') gets overwritten by (2, 'e')
        3: (3, "d"),  # only tuple with first element 3
    }
    assert result == expected


def test_flat_group_by_with_complex_predicate():
    numbers = [1, 4, 9, 16, 25, 36, 49]

    result = flat_group_by(numbers, lambda x: int(x**0.5) % 2 == 0)

    expected = {
        False: 49,  # sqrt: 1, 3, 5, 7 (odd) -> last is 49 (sqrt=7)
        True: 36,  # sqrt: 2, 4, 6 (even) -> last is 36 (sqrt=6)
    }
    assert result == expected


def test_flat_group_by_preserves_last_occurrence():
    items = ["first", "second", "third", "fourth"]

    result = flat_group_by(items, lambda x: "same_key")

    expected = {"same_key": "fourth"}
    assert result == expected


def test_flat_group_by_with_generator():
    def number_generator():
        for i in range(6):
            yield i

    result = flat_group_by(number_generator(), lambda x: x % 2)

    expected = {
        0: 4,  # even numbers: 0, 2, 4 -> last is 4
        1: 5,  # odd numbers: 1, 3, 5 -> last is 5
    }
    assert result == expected


def test_flat_group_by_with_none_values():
    items = [None, 1, None, 2, 3]
    result = flat_group_by(items, lambda x: x is None)

    expected = {
        True: None,  # last None value
        False: 3,  # last non-None value
    }
    assert result == expected


def test_flat_group_by_order_dependency():
    items1 = [1, 2, 3, 4]
    items2 = [4, 3, 2, 1]

    def predicate(x):
        return x % 2

    result1 = flat_group_by(items1, predicate)
    result2 = flat_group_by(items2, predicate)

    expected1 = {0: 4, 1: 3}  # last even is 4, last odd is 3
    expected2 = {0: 2, 1: 1}  # last even is 2, last odd is 1

    assert result1 == expected1
    assert result2 == expected2
    assert result1 != result2  # Results should be different


def test_flat_group_by_with_string_keys():
    numbers = [1, 10, 100, 2, 20, 200]

    result = flat_group_by(numbers, lambda x: f"{len(str(x))}_digits")

    expected = {
        "1_digits": 2,  # last 1-digit number
        "2_digits": 20,  # last 2-digit number
        "3_digits": 200,  # last 3-digit number
    }
    assert result == expected


def test_flat_group_by_maintains_original_type():
    class CustomClass:
        def __init__(self, value):
            self.value = value

        def __eq__(self, other):
            return isinstance(other, CustomClass) and self.value == other.value

    items = [CustomClass(1), CustomClass(2), CustomClass(3)]
    result = flat_group_by(items, lambda x: x.value % 2)

    expected = {
        1: CustomClass(3),  # last odd value
        0: CustomClass(2),  # last even value
    }
    assert result == expected
    assert isinstance(result[1], CustomClass)
    assert isinstance(result[0], CustomClass)
