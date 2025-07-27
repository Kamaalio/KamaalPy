from typing import TypedDict
from kamaaalpy.lists import group_by


class Person(TypedDict):
    name: str
    age: int
    city: str


def test_group_by_with_integers_by_even_odd():
    numbers = [1, 2, 3, 4, 5, 6]

    result = group_by(numbers, lambda x: x % 2 == 0)

    expected = {
        False: [1, 3, 5],  # odd numbers
        True: [2, 4, 6],  # even numbers
    }
    assert result == expected


def test_group_by_with_strings_by_length():
    words = ["cat", "dog", "elephant", "bee", "butterfly"]

    result = group_by(words, lambda x: len(x))

    expected = {3: ["cat", "dog", "bee"], 8: ["elephant"], 9: ["butterfly"]}
    assert result == expected


def test_group_by_with_strings_by_first_letter():
    words = ["apple", "banana", "cherry", "apricot", "blueberry"]

    result = group_by(words, lambda x: x[0])

    expected = {
        "a": ["apple", "apricot"],
        "b": ["banana", "blueberry"],
        "c": ["cherry"],
    }
    assert result == expected


def test_group_by_with_empty_list():
    result = group_by([], lambda x: x)

    assert result == {}


def test_group_by_with_single_item():
    result = group_by([42], lambda x: x > 0)

    expected = {True: [42]}
    assert result == expected


def test_group_by_with_all_same_key():
    numbers = [2, 4, 6, 8]

    result = group_by(numbers, lambda x: "even")

    expected = {"even": [2, 4, 6, 8]}
    assert result == expected


def test_group_by_with_dictionaries():
    people: list[Person] = [
        {"name": "Alice", "age": 25, "city": "New York"},
        {"name": "Bob", "age": 30, "city": "London"},
        {"name": "Charlie", "age": 25, "city": "New York"},
        {"name": "Diana", "age": 35, "city": "London"},
    ]

    result = group_by(people, lambda person: person["city"])

    expected: dict[str, list[Person]] = {
        "New York": [
            {"name": "Alice", "age": 25, "city": "New York"},
            {"name": "Charlie", "age": 25, "city": "New York"},
        ],
        "London": [
            {"name": "Bob", "age": 30, "city": "London"},
            {"name": "Diana", "age": 35, "city": "London"},
        ],
    }
    assert result == expected


def test_group_by_with_tuples():
    pairs = [(1, "a"), (2, "b"), (1, "c"), (3, "d"), (2, "e")]

    result = group_by(pairs, lambda pair: pair[0])

    expected = {1: [(1, "a"), (1, "c")], 2: [(2, "b"), (2, "e")], 3: [(3, "d")]}
    assert result == expected


def test_group_by_with_complex_predicate():
    numbers = [1, 4, 9, 16, 25, 36, 49]

    result = group_by(numbers, lambda x: int(x**0.5) % 2 == 0)

    expected = {
        False: [1, 9, 25, 49],  # sqrt: 1, 3, 5, 7 (odd)
        True: [4, 16, 36],  # sqrt: 2, 4, 6 (even)
    }
    assert result == expected


def test_group_by_preserves_order():
    items = ["z", "a", "b", "y", "c"]

    result = group_by(items, lambda x: x in "abc")

    expected = {False: ["z", "y"], True: ["a", "b", "c"]}
    assert result == expected


def test_group_by_with_generator():
    def number_generator():
        for i in range(5):
            yield i

    result = group_by(number_generator(), lambda x: x % 2)

    expected = {
        0: [0, 2, 4],  # even numbers
        1: [1, 3],  # odd numbers
    }
    assert result == expected


def test_group_by_with_none_values():
    items = [None, 1, None, 2, 3]

    result = group_by(items, lambda x: x is None)

    expected = {True: [None, None], False: [1, 2, 3]}
    assert result == expected
