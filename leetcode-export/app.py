#!/usr/bin/env python3
import argparse
import getpass
import logging
import os
from datetime import datetime
from string import Template
from typing import List, Dict

from leetcode import LeetCode
from leetcode_rest import Submission
from utils import language_to_extension, remove_special_characters

PROBLEM_INFO_TEMPLATE = Template('''${questionId} - ${title}
${difficulty} - https://leetcode.com/problems/${titleSlug}/

${content}
''')


def parse_args():
    parser = argparse.ArgumentParser(description='Export LeetCode solutions')
    parser.add_argument('--username', type=str, required=False, help='LeetCode username')
    parser.add_argument('--password', type=str, required=False, help='LeetCode password')
    parser.add_argument('--folder', type=str, required=False, help='Output folder', default='out')
    parser.add_argument('--cookies', type=str, required=False, help='LeetCode cookies')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Enable verbose logging details')
    parser.add_argument('-vv', '--extra-verbose', dest='extra_verbose', action='store_true',
                        help='Enable more verbose logging details')
    parser.set_defaults(verbose=False, extra_verbose=False)

    return parser.parse_args()


class App(object):
    args = parse_args()

    # Set logging level based on program arguments
    level = logging.WARNING
    if args.verbose:
        level = logging.INFO
    if args.extra_verbose:
        level = logging.DEBUG

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s",
        handlers=[
            logging.FileHandler("debug.log"),
            logging.StreamHandler()
        ]
    )

    leetcode = LeetCode()

    if not args.cookies:
        username = args.username
        password = args.password

        if not username:
            username = input("Insert LeetCode username: ")
        if not password:
            password = getpass.getpass(prompt="Insert LeetCode password: ")
        if not leetcode.log_in(args.username, args.password):
            print(
                "Login not successful! You might have entered the wrong username/password or you need to complete the reCAPTCHA. If you need to complete the captcha, log in with the cookies instead. Check the log for more informaton.")
            exit(1)
    else:
        leetcode.set_cookies(args.cookies)

    if not os.path.exists(args.folder):
        os.mkdir(args.folder)
    os.chdir(args.folder)

    submissions: Dict[str, List[Submission]] = leetcode.get_submissions()

    for slug in submissions:
        logging.info(f"Processing {slug}")
        if not os.path.exists(slug):
            os.mkdir(slug)
        else:
            logging.info(f"Folder {slug} already exists")
        os.chdir(slug)
        problem_info = leetcode.get_problem(slug)
        info_filename = f"{problem_info.questionId} - {slug}.txt"
        if not os.path.exists(info_filename):
            info_file = open(info_filename, 'w+')
            info_file.write(PROBLEM_INFO_TEMPLATE.substitute(**problem_info.__dict__))
            info_file.close()

        for sub in submissions[slug]:
            sub_filename = f"{datetime.fromtimestamp(sub.timestamp).strftime('%Y-%m-%d %H.%M.%S')} - {sub.status_display} - runtime {remove_special_characters(sub.runtime)} - memory {remove_special_characters(sub.memory)}.{language_to_extension(sub.lang)}"
            if not os.path.exists(sub_filename):
                logging.info(f"Writing {slug}/{sub_filename}")
                sub_file = open(sub_filename, 'w+')
                sub_file.write(sub.code)
                sub_file.close()
            else:
                logging.info(f"{slug}/{sub_filename} already exists, skipping it")

        os.chdir("..")
