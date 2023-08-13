import pytest

from kamaaalpy.dicts import omit_empty


@pytest.mark.parametrize("empty_input", [(False), (0), (None), (""), ({}), ([])])
def test_omit_empty_with_empty_values(empty_input):
    input_dict = {"yes": True, "no": empty_input}

    assert omit_empty(input_dict) == {"yes": True}
    assert input_dict == {"yes": True, "no": empty_input}


@pytest.mark.parametrize(
    "filled_input", [(True), (1), ("Kamaal"), ({"in": "out"}), ([1])]
)
def test_omit_empty_with_filled_values(filled_input):
    input_dict = {"yes": filled_input}

    assert omit_empty(input_dict) == {"yes": filled_input}
    assert input_dict == {"yes": filled_input}
