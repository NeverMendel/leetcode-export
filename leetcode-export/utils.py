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


def language_to_extension(language: str) -> str:
    return FILE_EXTENSIONS[language]


def remove_special_characters(string: str) -> str:
    for el in SPECIAL_CHARACTERS_FILENAME:
        string = string.replace(el, '')
    return string
