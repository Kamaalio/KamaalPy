from kamaaalpy.lists import find_index


def test_find_index():
    input_list = [1, 2, 3]

    assert find_index(input_list, lambda item: item == 1) == 0
    assert find_index(input_list, lambda item: item == 2) == 1
    assert find_index(input_list, lambda item: item == 3) == 2


def test_find_index_not_found():
    input_list = [1, 2, 3]

    assert find_index(input_list, lambda item: item == 4) is None
