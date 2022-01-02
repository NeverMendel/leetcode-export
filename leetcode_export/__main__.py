#!/usr/bin/env python3
import argparse
import logging
import os
from string import Template
from typing import List, Dict

from leetcode_export.leetcode import LeetCode
from leetcode_export.leetcode_rest import Submission

PROBLEM_CONTENT_TEMPLATE = Template('''${question_id} - ${title}
${difficulty} - https://leetcode.com/problems/${title_slug}/

${content}
''')


def parse_args():
    parser = argparse.ArgumentParser(description='Export LeetCode solutions')
    parser.add_argument('--cookies', type=str, help='Set LeetCode cookies')
    parser.add_argument('--folder', type=str, default='.', help='Output folder')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Enable verbose logging details')
    parser.add_argument('-vv', '--extra-verbose', dest='extra_verbose', action='store_true',
                        help='Enable more verbose logging details')
    parser.add_argument('--problem-filename', type=str, default='${question_id} - ${title_slug}.txt',
                        help='Problem description filename format')
    parser.add_argument('--submission-filename', type=str,
                        default='${date_formatted} - ${status_display} - runtime ${runtime} - memory ${memory}.${extension}',
                        help='Submission filename format')
    parser.set_defaults(verbose=False, extra_verbose=False)

    return parser.parse_args()


def main():
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
    cookies = args.cookies

    if not cookies:
        cookies = input("Insert LeetCode cookies: ")

    if not leetcode.set_cookies(cookies):
        print(
            "Cookies not valid. Copy them from the Network tab of your browser by clicking on any leetcode.com request and going in Request Headers > cookie.")
        exit(1)

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


if __name__ == '__main__':
    main()
