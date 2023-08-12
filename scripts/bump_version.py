import sys
import tomllib
from pathlib import Path

import tomli_w
from packaging import version


def main():
    assert len(sys.argv) == 2

    new_version = version.parse(sys.argv[1])
    pyproject = Path("pyproject.toml")
    pyproject_toml = tomllib.loads(pyproject.read_text())
    current_version = version.parse(pyproject_toml["project"]["version"])
    if current_version == new_version:
        print("No version to update")
        return

    assert current_version <= new_version

    pyproject_toml["project"]["version"] = str(new_version)
    pyproject_toml_string = tomli_w.dumps(pyproject_toml)
    pyproject.write_text(pyproject_toml_string)
    print("Updated pyproject.toml")


if __name__ == "__main__":
    main()
