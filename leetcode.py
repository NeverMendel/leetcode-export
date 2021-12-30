from dataclasses import dataclass
from time import sleep
from typing import Dict, List

import requests
from dataclasses_json import dataclass_json
from selenium import webdriver

LOGIN_URL = 'https://leetcode.com/accounts/login/'
SUBMISSIONS_API_URL = 'https://leetcode.com/api/submissions/?offset={}&limit={}'
PROBLEM_URL = 'https://leetcode.com/problems/'
GRAPHQL_URL = 'https://leetcode.com/graphql'

FILE_EXTENSION = {
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


@dataclass_json
@dataclass
class Submission:
    id: int
    lang: str
    time: str
    timestamp: int
    status_display: str
    runtime: str
    url: str
    is_pending: str
    title: str
    memory: str
    code: str
    compare_result: str
    title_slug: str


@dataclass
class Problem:
    problem_id: int
    title: str
    slug: str
    difficulty: str
    description: str
    test_cases: str


def question_data(slug):
    return {
        "operationName": "questionData",
        "variables": {
            "titleSlug": slug
        },
        "query": """query questionData($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                questionId
                questionFrontendId
                boundTopicId
                title
                titleSlug
                content
                difficulty
                sampleTestCase
            }
        }"""
    }


def get_problem_info(cookies: str, slug: str):
    response = requests.post(
        GRAPHQL_URL,
        json=question_data(slug),
        headers={'Cookie': cookies})
    return response


def valid_cookies(cookies: str) -> bool:
    return True


def get_cookies(username: str, password: str) -> str:
    driver = webdriver.Chrome()
    driver.get(LOGIN_URL)

    return ''


def get_submissions(cookies: str) -> Dict[str, List[Submission]]:
    dictionary: Dict[str, List[Submission]] = {}
    batch_size = 20
    offset = 0
    while True:
        print(f"getting batch #{offset + 1}")
        response = requests.get(
            SUBMISSIONS_API_URL.format(offset, batch_size),
            headers={'Cookie': cookies})
        json_response = response.json()
        if 'detail' in json_response:
            print(json_response['detail'])
        if 'submissions_dump' in json_response:
            for submission_dict in json_response['submissions_dump']:
                submission = Submission.from_dict(submission_dict)
                if submission.title_slug not in dictionary:
                    dictionary[submission.title_slug] = []
                dictionary[submission.title_slug].append(submission)
        if 'has_next' not in json_response or not json_response['has_next']:
            break
        offset += batch_size
        sleep(2)
    return dictionary
