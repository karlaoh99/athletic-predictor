import json
from typing import Tuple


def get_country_and_name(file_name: str) -> Tuple[str, str]:
    splitted_list = file_name.split('_')
    country = splitted_list[0]
    name = ' '.join(splitted_list[1:])
    return country, name


def load_json(file: str) -> dict:
    """Loads a json file and returns a dictionary."""

    try:
        with open(file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except: 
        return {}


def save_json(data: dict, file: str) -> None:
    """Saves a dictionary in a json file."""

    with open(file, 'w+', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


__all__ = [
    "get_country_and_name",
    "load_json",
    "save_json",
]