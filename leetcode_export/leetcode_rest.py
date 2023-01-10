from dataclasses import dataclass

from dataclasses_json import dataclass_json

BASE_URL = "https://leetcode.com"
LOGIN_URL = "https://leetcode.com/accounts/login/"
SUBMISSIONS_API_URL = "https://leetcode.com/api/submissions/?offset={}&limit={}"
PROBLEM_URL = "https://leetcode.com/problems/"


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
    date_formatted: str
    extension: str
