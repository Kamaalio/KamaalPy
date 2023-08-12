from kamaaalpy.lists import removed


def test_removed():
    input_list = [1, 2, 3]

    assert removed(input_list, 0) == [2, 3]
    assert removed(input_list, 1) == [1, 3]
    assert input_list == [1, 2, 3]


def test_removed_with_out_of_range_index():
    input_list = [1, 2, 3]

    assert removed(input_list, 3) == [1, 2, 3]
    assert input_list == [1, 2, 3]
