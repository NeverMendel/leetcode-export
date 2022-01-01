import logging
from datetime import datetime
from time import sleep
from typing import Dict, List

import requests

from leetcode_export.leetcode_graphql import GRAPHQL_URL, question_detail_json, Problem
from leetcode_export.leetcode_rest import LOGIN_URL, SUBMISSIONS_API_URL, Submission, BASE_URL
from leetcode_export.utils import language_to_extension, remove_special_characters


class LeetCode(object):
    def __init__(self):
        logging.debug("LeetCode class instantiated")
        self.cookies = ''
        self.user_logged = False

    def log_in(self, username: str, password: str) -> bool:
        session = requests.Session()

        session.get(LOGIN_URL)

        csrftoken = session.cookies.get('csrftoken')

        headers = {'Origin': BASE_URL, 'Referer': LOGIN_URL}
        payload = {'csrfmiddlewaretoken': csrftoken, 'login': username, 'password': password}

        response_post = session.post(LOGIN_URL, headers=headers,
                                     data=payload)  # sent using the same session, headers will also contain the cookies of the previous get request

        if response_post.status_code == 200:
            self.cookies = f"csrftoken={session.cookies.get('csrftoken')};LEETCODE_SESSION={session.cookies.get('LEETCODE_SESSION')};"
            self.user_logged = True
            logging.info("Login successful")
            return True
        else:
            logging.warning(response_post.json())
            return False

    def set_cookies(self, cookies: str):
        self.cookies = cookies
        self.user_logged = True
        logging.info("Cookies set successful")

    def is_user_logged(self) -> bool:
        if self.user_logged:
            logging.debug("User is logged in")
        else:
            logging.debug("User is not logged in")
        return self.user_logged

    def get_problem(self, slug: str) -> Problem:
        response = requests.post(
            GRAPHQL_URL,
            json=question_detail_json(slug),
            headers={'Cookie': self.cookies})
        if 'data' in response.json() and 'question' in response.json()['data']:
            return Problem.from_dict(response.json()['data']['question'])

    def get_submissions(self) -> Dict[str, List[Submission]]:
        dictionary: Dict[str, List[Submission]] = {}
        current = 0
        response_json: Dict = {'has_next': True}
        while 'detail' not in response_json and 'has_next' in response_json and response_json['has_next']:
            logging.info(f"Exporting submissions from {current} to {current + 20}")
            response_json = requests.get(
                SUBMISSIONS_API_URL.format(current),
                headers={'Cookie': self.cookies}).json()
            if 'submissions_dump' in response_json:
                for submission_dict in response_json['submissions_dump']:
                    submission_dict['runtime'] = submission_dict['runtime'].replace(' ', '')
                    submission_dict['memory'] = submission_dict['memory'].replace(' ', '')
                    submission_dict['date_formatted'] = datetime.fromtimestamp(submission_dict['timestamp']).strftime(
                        '%Y-%m-%d %H.%M.%S')
                    submission_dict['extension'] = language_to_extension(submission_dict['lang'])
                    for key in submission_dict:
                        if type(submission_dict[key]) == str and key != 'url' and key != 'code':
                            submission_dict[key] = remove_special_characters(submission_dict[key])
                    submission = Submission.from_dict(submission_dict)
                    if submission.title_slug not in dictionary:
                        dictionary[submission.title_slug] = []
                    dictionary[submission.title_slug].append(submission)
                sleep(1)
            current += 20
        if 'detail' in response_json:
            logging.warning(response_json['detail'])
        return dictionary
