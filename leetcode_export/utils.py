import re
from typing import Dict

VALID_PROGRAMMING_LANGUAGES = [
    "python",
    "python3",
    "pythondata",
    "c",
    "cpp",
    "csharp",
    "java",
    "kotlin",
    "mysql",
    "mssql",
    "oraclesql",
    "javascript",
    "html",
    "php",
    "golang",
    "scala",
    "pythonml",
    "rust",
    "ruby",
    "bash",
    "swift",
    "typescript",
    "elixir",
    "erlang",
    "racket",
    "dart",
]

FILE_EXTENSIONS = {
    "python": "py",
    "python3": "py",
    "pythondata": "pd.py",
    "c": "c",
    "cpp": "cpp",
    "csharp": "cs",
    "java": "java",
    "kotlin": "kt",
    "mysql": "sql",
    "mssql": "sql",
    "oraclesql": "sql",
    "javascript": "js",
    "html": "html",
    "php": "php",
    "golang": "go",
    "scala": "scala",
    "pythonml": "py",
    "rust": "rs",
    "ruby": "rb",
    "bash": "sh",
    "swift": "swift",
    "typescript": "ts",
    "elixir": "ex",
    "erlang": "erl",
    "racket": "rkt",
    "dart": "dart",
}

SPECIAL_CHARACTERS_FILENAME = ["/", "\\", ":", "*", "?", '"', '"', "<", ">", "|"]
_regex_camelcase_to_snakecase1 = re.compile(r"(.)([A-Z][a-z]+)")
_regex_camelcase_to_snakecase2 = re.compile("([a-z0-9])([A-Z])")

REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
}


def language_to_extension(language: str) -> str:
    """
    Return extension format for given programming language
    :param language: programming language
    :return: str extension format
    """
    return FILE_EXTENSIONS[language]


def remove_special_characters(string: str) -> str:
    """
    Returns a new string where without any character that is not allowed in windows filenames
    :param string: string to process
    :return: str string without special characters
    """
    for el in SPECIAL_CHARACTERS_FILENAME:
        string = string.replace(el, "")
    return string


def camelcase_to_snakecase(string: str) -> str:
    """
    Returns a new string transforming a CamelCase string into snake_case
    :param string: CamelCase string to process
    :return: str snake_case string
    """
    subbed = _regex_camelcase_to_snakecase1.sub(r"\1_\2", string)
    return _regex_camelcase_to_snakecase2.sub(r"\1_\2", subbed).lower()


def dict_camelcase_to_snakecase(dictionary: Dict[str, any]) -> Dict[str, any]:
    """
    Returns a new dictionary where keys are transformed from CamelCase into snake_case
    :param dictionary: original dictionary
    :return: Dict[str, any] new dictionary with snake_case keys
    """
    new_dict: Dict[str, any] = {}
    for key in dictionary:
        new_dict[camelcase_to_snakecase(key)] = dictionary[key]
    return new_dict
