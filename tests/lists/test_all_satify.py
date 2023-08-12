from kamaaalpy.lists import all_satisfy


def test_find_index():
    input_list = [1, 2, 3]

    assert all_satisfy(input_list, lambda item: item < 4)
    assert not all_satisfy(input_list, lambda item: item > 4)
