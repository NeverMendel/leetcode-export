#!/usr/bin/env python3
import argparse
import getpass
import logging
import os
from string import Template
from typing import List, Dict

from leetcode import LeetCode
from leetcode_rest import Submission

PROBLEM_CONTENT_TEMPLATE = Template('''${questionId} - ${title}
${difficulty} - https://leetcode.com/problems/${titleSlug}/

${content}
''')


def parse_args():
    parser = argparse.ArgumentParser(description='Export LeetCode solutions')
    parser.add_argument('--username', type=str, required=False, help='Set LeetCode username')
    parser.add_argument('--password', type=str, required=False, help='Set LeetCode password')
    parser.add_argument('--folder', type=str, required=False, help='Output folder', default='out')
    parser.add_argument('--cookies', type=str, required=False, help='Set LeetCode cookies')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Enable verbose logging details')
    parser.add_argument('-vv', '--extra-verbose', dest='extra_verbose', action='store_true',
                        help='Enable more verbose logging details')
    parser.add_argument('--problem-filename', type=str, default='${questionId} - ${titleSlug}.txt',
                        help='Problem description filename format')
    parser.add_argument('--submission-filename', type=str,
                        default='${date_formatted} - ${status_display} - runtime ${runtime} - memory ${memory}.${extension}',
                        help='Submission filename format')
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

    problem_template = Template(args.problem_filename)
    submission_template = Template(args.submission_filename)

    leetcode = LeetCode()
    username = ''
    password = ''
    cookies = ''

    # Login into leetcode
    if (not args.username or not args.password) and not args.cookies:
        choice = input("How do you want to login?\n  1 - Username and Password\n  2 - Cookies\n")
        while choice != '1' and choice != '2':
            print("Choice not valid, input 1 or 2")
            choice = input("How do you want to login?\n  1 - Username and Password\n  2 - Cookies\n")

        if choice == '1':
            username = input("Insert LeetCode username: ")
            password = getpass.getpass(prompt="Insert LeetCode password: ")
        else:
            cookies = input("Insert LeetCode cookies: ")
    else:
        username = args.username
        password = args.password
        cookies = args.cookies

    if username and password and not leetcode.log_in(args.username, args.password):
        print(
            "Login not successful! You might have entered the wrong username/password or you need to complete the reCAPTCHA. If you need to complete the reCAPTCHA, log in with the cookies instead. Check the log for more information.")
        exit(1)

    if cookies:
        leetcode.set_cookies(cookies)

    # Create output folder if it doesn't already exist
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
        problem_description = leetcode.get_problem(slug)
        info_filename = problem_template.substitute(**problem_description.__dict__)
        if not os.path.exists(info_filename):
            info_file = open(info_filename, 'w+')
            info_file.write(PROBLEM_CONTENT_TEMPLATE.substitute(**problem_description.__dict__))
            info_file.close()

        for sub in submissions[slug]:
            sub_filename = submission_template.substitute(**sub.__dict__)
            if not os.path.exists(sub_filename):
                logging.info(f"Writing {slug}/{sub_filename}")
                sub_file = open(sub_filename, 'w+')
                sub_file.write(sub.code)
                sub_file.close()
            else:
                logging.info(f"{slug}/{sub_filename} already exists, skipping it")

        os.chdir("..")
