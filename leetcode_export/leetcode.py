import datetime
import logging
from time import sleep
from typing import Dict, Iterator

import requests

from leetcode_export.leetcode_graphql import GRAPHQL_URL, question_detail_json, Problem
from leetcode_export.leetcode_rest import LOGIN_URL, SUBMISSIONS_API_URL, Submission, BASE_URL
from leetcode_export.utils import language_to_extension, remove_special_characters, dict_camelcase_to_snakecase


class LeetCode(object):
    def __init__(self):
        logging.debug("LeetCode class instantiated")
        self.session = requests.Session()
        self.user_logged = False
        self.user_logged_expiration = datetime.datetime.now()

    def log_in(self, username: str, password: str) -> bool:
        self.session.get(LOGIN_URL)

        csrftoken = self.session.cookies.get('csrftoken')

        headers = {'Origin': BASE_URL, 'Referer': LOGIN_URL}
        payload = {'csrfmiddlewaretoken': csrftoken, 'login': username, 'password': password}

        response_post = self.session.post(LOGIN_URL, headers=headers,
                                          data=payload)  # sent using the same session, headers will also contain the cookies of the previous get request

        if response_post.status_code == 200 and self.is_user_logged():
            # self.cookies = f"csrftoken={self.session.cookies.get('csrftoken')};LEETCODE_SESSION={self.session.cookies.get('LEETCODE_SESSION')};"
            logging.info("Login successful")
            return True
        else:
            logging.warning(response_post.json())
            return False

    def set_cookies(self, cookies: str) -> bool:
        '''
        Log in to LeetCode using cookies
        :param cookies: string with cookies to set
        :return: bool, true if login is successful, false otherwise
        '''
        cookies_list = cookies.split(';')
        cookies_list = map(lambda el: el.split('='), cookies_list)
        for cookies in cookies_list:
            self.session.cookies.set(cookies[0].strip(), cookies[1].strip())
        if self.is_user_logged():
            logging.info("Cookies set successful")
            return True
        else:
            logging.warning("Cookies set failed")
            return False

    def is_user_logged(self) -> bool:
        '''
        Check if user is logged in LeetCode account
        :return: bool, true if user is logged in, false otherwise
        '''
        if self.user_logged and datetime.datetime.now() < self.user_logged_expiration:
            return True
        cookie_dict = self.session.cookies.get_dict()
        if 'csrftoken' in cookie_dict and 'LEETCODE_SESSION' in cookie_dict:
            get_request = self.session.get(SUBMISSIONS_API_URL.format(0, 1))
            sleep(1)  # cooldown time for get request
            if 'detail' not in get_request.json():
                logging.debug("User is logged in")
                self.user_logged = True
                self.user_logged_expiration = datetime.datetime.now() + datetime.timedelta(hours=5)
                return True
        logging.debug("User is not logged in")
        return False

    def get_problem(self, slug: str) -> Problem:
        '''
        Get LeetCode problem info
        :param slug: problem identifier
        :return: Problem
        '''
        response = self.session.post(
            GRAPHQL_URL,
            json=question_detail_json(slug))
        if 'data' in response.json() and 'question' in response.json()['data']:
            problem_dict = dict_camelcase_to_snakecase(response.json()['data']['question'])
            return Problem.from_dict(problem_dict)

    def get_submissions(self) -> Iterator[Submission]:
        '''
        Get submissions for logged user
        :return: Iterator[Submission], LeetCode submission
        '''
        if not self.is_user_logged():
            logging.warning("Trying to get user submissions while user is not logged in")
            return None

        current = 0
        response_json: Dict = {'has_next': True}
        while 'detail' not in response_json and 'has_next' in response_json and response_json['has_next']:
            logging.info(f"Exporting submissions from {current} to {current + 20}")
            response_json = self.session.get(
                SUBMISSIONS_API_URL.format(current, 20)).json()
            if 'submissions_dump' in response_json:
                for submission_dict in response_json['submissions_dump']:
                    submission_dict['runtime'] = submission_dict['runtime'].replace(' ', '')
                    submission_dict['memory'] = submission_dict['memory'].replace(' ', '')
                    submission_dict['date_formatted'] = datetime.datetime.fromtimestamp(
                        submission_dict['timestamp']).strftime(
                        '%Y-%m-%d %H.%M.%S')
                    submission_dict['extension'] = language_to_extension(submission_dict['lang'])
                    for key in submission_dict:
                        if type(submission_dict[key]) == str and key != 'url' and key != 'code':
                            submission_dict[key] = remove_special_characters(submission_dict[key])
                    submission = Submission.from_dict(submission_dict)
                    yield submission

            current += 20
            sleep(1)
        if 'detail' in response_json:
            logging.warning(response_json['detail'])
