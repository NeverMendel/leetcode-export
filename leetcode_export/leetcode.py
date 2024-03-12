"""
LeetCode Python APIs for retrieving submitted problems and problem statements.
"""

import datetime
import logging
from time import sleep
from typing import Dict, Iterator

import requests

from leetcode_export.leetcode_graphql import GRAPHQL_URL, question_detail_json, Problem
from leetcode_export.leetcode_rest import (
    BASE_URL,
    LOGIN_URL,
    SUBMISSIONS_API_URL,
    Submission,
)
from leetcode_export.utils import (
    dict_camelcase_to_snakecase,
    language_to_extension,
    remove_special_characters,
    REQUEST_HEADERS,
)


class LeetCode(object):
    def __init__(self):
        logging.debug("LeetCode class instantiated")
        self.session = requests.Session()
        self.session.headers.update(REQUEST_HEADERS)
        self.user_logged = False
        self.user_logged_expiration = datetime.datetime.now()

    def log_in(self, username: str, password: str) -> bool:
        """
        Log in to LeetCode using username and password
        :param username: LeetCode username
        :param password: LeetCode password
        :return: bool, true if login is successful, false otherwise
        """
        self.session.get(LOGIN_URL)

        csrftoken = self.session.cookies.get("csrftoken")

        headers = {"Origin": BASE_URL, "Referer": LOGIN_URL}
        payload = {
            "csrfmiddlewaretoken": csrftoken,
            "login": username,
            "password": password,
        }

        response_post = self.session.post(
            LOGIN_URL, headers=headers, data=payload
        )  # sent using the same session, headers will also contain the cookies of the previous get request

        if response_post.status_code == 200 and self.is_user_logged():
            # self.cookies = f"csrftoken={self.session.cookies.get('csrftoken')};LEETCODE_SESSION={self.session.cookies.get('LEETCODE_SESSION')};"
            logging.info("Login successful")
            return True
        else:
            logging.warning(response_post.json())
            return False

    def set_cookies(self, cookies: str) -> bool:
        """
        Log in to LeetCode using cookies
        :param cookies: string with cookies to set
        :return: bool, true if login is successful, false otherwise
        """
        valid_cookies = True
        cookie_dict = {}

        for cookie in cookies.split(";"):
            cookie_split = [el.strip() for el in cookie.split("=", 1)]
            if len(cookie_split) != 2:
                valid_cookies = False
                break
            cookie_dict[cookie_split[0]] = cookie_split[1]

        valid_cookies = (
            valid_cookies
            and "csrftoken" in cookie_dict
            and "LEETCODE_SESSION" in cookie_dict
        )
        if not valid_cookies:
            logging.error(
                "Cookie format not valid. Expected: 'csrftoken=value1;LEETCODE_SESSION=value2;...'"
            )
            return False

        for cookie_key, cookie_value in cookie_dict.items():
            self.session.cookies.set(cookie_key, cookie_value)
        if self.is_user_logged():
            logging.info("Cookie set successful")
            return True
        return False

    def is_user_logged(self) -> bool:
        """
        Check if user is logged in LeetCode account
        :return: bool, true if user is logged in, false otherwise
        """
        if self.user_logged and datetime.datetime.now() < self.user_logged_expiration:
            return True
        cookie_dict = self.session.cookies.get_dict()
        if "csrftoken" in cookie_dict and "LEETCODE_SESSION" in cookie_dict:
            get_request = self.session.get(SUBMISSIONS_API_URL.format(0, 1))
            logging.debug(get_request.text)
            sleep(1)  # cooldown time for get request
            if "detail" not in get_request.json():
                logging.debug("User is logged in")
                self.user_logged = True
                self.user_logged_expiration = (
                    datetime.datetime.now() + datetime.timedelta(hours=5)
                )
                return True
        logging.error("User is not logged in or account is invalid!")
        return False

    def get_problem_statement(self, slug: str) -> Problem:
        """
        Get LeetCode problem statement
        :param slug: problem identifier
        :return: Problem
        """
        response = self.session.post(GRAPHQL_URL, json=question_detail_json(slug))
        if "data" in response.json() and "question" in response.json()["data"]:
            problem_dict = dict_camelcase_to_snakecase(
                response.json()["data"]["question"]
            )
            return Problem.from_dict(problem_dict)

    def get_submissions(self) -> Iterator[Submission]:
        """
        Get submissions for logged user
        :return: Iterator[Submission], LeetCode submission
        """
        if not self.is_user_logged():
            logging.error("Trying to get user submissions while user is not logged in")
            return None

        current = 0
        response_json: Dict = {"has_next": True}
        while (
            "detail" not in response_json
            and "has_next" in response_json
            and response_json["has_next"]
        ):
            logging.debug(f"Exporting submissions from {current} to {current + 20}")
            response = self.session.get(SUBMISSIONS_API_URL.format(current, 20))
            logging.debug(response.content)
            response_json = response.json()
            if "submissions_dump" in response_json:
                for submission_dict in response_json["submissions_dump"]:
                    submission_dict["runtime"] = submission_dict["runtime"].replace(
                        " ", ""
                    )
                    submission_dict["memory"] = submission_dict["memory"].replace(
                        " ", ""
                    )
                    submission_dict["date_formatted"] = datetime.datetime.fromtimestamp(
                        submission_dict["timestamp"]
                    ).strftime("%Y-%m-%d %H.%M.%S")
                    submission_dict["extension"] = language_to_extension(
                        submission_dict["lang"]
                    )
                    for key in submission_dict:
                        if (
                            type(submission_dict[key]) == str
                            and key != "url"
                            and key != "code"
                        ):
                            submission_dict[key] = remove_special_characters(
                                submission_dict[key]
                            )
                    submission = Submission.from_dict(submission_dict)
                    yield submission

            current += 20
            sleep(5)  # cooldown time for get request
        if "detail" in response_json:
            logging.warning(
                'LeetCode API error, detail found in response_json. response_json["detail"]: '
                + str(response_json["detail"])
            )
