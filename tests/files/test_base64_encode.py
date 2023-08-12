from pathlib import Path

import pytest
from kamaaalpy.files import base64_encode


def test_base64_encode():
    input_file = Path("tests/samples/16.png")
    expected_output_file = Path("tests/samples/16.b64")

    assert input_file.exists()
    assert base64_encode(input_file) == expected_output_file.read_bytes()


def test_base64_encode_folder():
    input_folder = Path("tests/samples")

    assert input_folder.exists()
    assert input_folder.is_dir()
    with pytest.raises(IsADirectoryError):
        base64_encode(input_folder)


def test_base64_encode_does_not_exists():
    input_file = Path("tests/samples/17.png")

    assert not input_file.exists()
    with pytest.raises(FileNotFoundError):
        assert base64_encode(input_file)
