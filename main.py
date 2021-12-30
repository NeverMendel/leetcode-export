#!/usr/bin/env python3
import argparse
import os.path
from string import Template

import leetcode

PROBLEM_INFO_TEMPLATE = Template('''${problem_id} - ${title}
${difficulty} - https://leetcode.com/problems/${slug}/"

${description}

${test_cases}
''')


def parse_args():
    parser = argparse.ArgumentParser(description='Export LeetCode solutions')
    parser.add_argument('--username', type=str, required=False, help='LeetCode username')
    parser.add_argument('--password', type=str, required=False, help='LeetCode password')
    parser.add_argument('--folder', type=str, required=False, help='Output folder', default='out')
    parser.add_argument('--cookies', type=str, required=False, help='LeetCode cookies')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    cookies = args.cookies

    print(leetcode.get_submissions(cookies))
    # if not cookies or not leetcode.valid_cookies(cookies):
    #     if not args.username:
    #         print("Insert LeetCode username: ")
    #         args.username = input()
    #
    #     if not args.password:
    #         print("Insert LeetCode username: ")
    #         args.password = input()
    #
    #     if not os.path.exists(args.folder):
    #         os.mkdir(args.folder)
    #     os.chdir(args.folder)
    #     cookies = leetcode.get_cookies(args.username, args.password)
    #
    # solved_problems = leetcode.get_solved_problem_slugs(cookies)
    #
    # for slug in solved_problems:
    #     if not os.path.exists(slug):
    #         os.mkdir(slug)
    #     os.chdir(slug)
    #     problem_info = leetcode.get_problem(cookies, slug)
    #     info_filename = f"{problem_info.slug}.txt"
    #     if not os.path.exists(info_filename):
    #         info_file = open(info_filename, 'w+')
    #         info_file.write(PROBLEM_INFO_TEMPLATE.substitute(**problem_info.__dict__))
    #         info_file.close()
    #
    #     submissions = leetcode.get_submissions(cookies, slug)
    #
    #     for sub in submissions:
    #         sub_filename = f"{sub.submission_date.strftime('%Y-%m-%d %H-%M-%S')} - {sub.status} - runtime: {sub.runtime} - memory: {sub.memory}.{sub.extension}"
    #         if not os.path.exists(sub_filename):
    #             sub_file = open(sub_filename, 'w+')
    #             sub_file.write(sub.code)
    #             sub_file.close()
