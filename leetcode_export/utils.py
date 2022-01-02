import re
from typing import Dict

FILE_EXTENSIONS = {
    "python": 'py',
    "python3": 'py',
    "c": 'c',
    "cpp": 'cpp',
    "csharp": 'cs',
    "java": 'java',
    "kotlin": 'kt',
    "mysql": 'sql',
    "mssql": 'sql',
    "oraclesql": 'sql',
    "javascript": 'js',
    "html": 'html',
    "php": 'php',
    "golang": 'go',
    "scala": 'scala',
    "pythonml": 'py',
    "rust": 'rs',
    "ruby": 'rb',
    "bash": 'sh',
    "swift": 'swift'
}

SPECIAL_CHARACTERS_FILENAME = ['/', '\\', ':', '*', '?', '"', '"', '<', '>', '|']
_regex_camelcase_to_snakecase1 = re.compile(r'(.)([A-Z][a-z]+)')
_regex_camelcase_to_snakecase2 = re.compile('([a-z0-9])([A-Z])')


def language_to_extension(language: str) -> str:
    return FILE_EXTENSIONS[language]


def remove_special_characters(string: str) -> str:
    for el in SPECIAL_CHARACTERS_FILENAME:
        string = string.replace(el, '')
    return string


def camelcase_to_snakecase(string: str) -> str:
    subbed = _regex_camelcase_to_snakecase1.sub(r'\1_\2', string)
    return _regex_camelcase_to_snakecase2.sub(r'\1_\2', subbed).lower()


def dict_camelcase_to_snakecase(dictionary: Dict[str, any]) -> Dict[str, any]:
    new_dict: Dict[str, any] = {}
    for key in dictionary:
        new_dict[camelcase_to_snakecase(key)] = dictionary[key]
    return new_dict
