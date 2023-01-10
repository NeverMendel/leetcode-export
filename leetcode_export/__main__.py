"""
LeetCode Export.

Export your LeetCode submissions and related problem statements.
"""
import argparse
import logging
import os
from string import Template
from typing import Set

from leetcode_export._version import __version__
from leetcode_export.leetcode import LeetCode
from leetcode_export.utils import VALID_PROGRAMMING_LANGUAGES


def parse_args():
    parser = argparse.ArgumentParser(
        description="Export LeetCode submissions",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("--cookies", type=str, help="set LeetCode cookies")
    parser.add_argument("--folder", type=str, default=".", help="set output folder")
    parser.add_argument(
        "--problem-folder-name",
        type=str,
        default="${question_id}-${title_slug}",
        help="problem folder name format",
    )
    parser.add_argument(
        "--problem-statement-filename",
        type=str,
        default="${question_id}-${title_slug}.html",
        help="problem statement filename format",
    )
    parser.add_argument(
        "--problem-statement-content",
        type=str,
        default="<h1>${question_id} - ${title}</h1><h2>Difficulty: ${difficulty} - "
        + '<a href="https://leetcode.com/problems/${title_slug}/">${title_slug}</a></h2>${content}',
        help="problem statement content format",
    )
    parser.add_argument(
        "--submission-filename",
        type=str,
        default="${date_formatted} - ${status_display} - runtime ${runtime} - memory ${memory}.${extension}",
        help="submission filename format",
    )
    parser.add_argument(
        "--only-accepted",
        dest="only_accepted",
        action="store_true",
        help="save accepted submissions only",
    )
    parser.add_argument(
        "--language",
        dest="language_unprocessed",
        type=str,
        help="only save submissions for the specified programming languages (eg. '--language=python,python3,cpp,java,golang')\n"
        + "supported languages: 'python', 'python3', 'c', 'cpp', 'csharp', 'java', 'kotlin', 'mysql', 'mssql', 'oraclesql',\n"
        + "                     'javascript', 'html', 'php', 'golang', 'scala', 'pythonml', 'rust', 'ruby', 'bash', 'swift'",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        help="enable verbose logging details",
    )
    parser.add_argument(
        "-vv",
        "--extra-verbose",
        dest="extra_verbose",
        action="store_true",
        help="enable more verbose logging details",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version="%(prog)s {version}".format(version=__version__),
    )
    parser.set_defaults(verbose=False, extra_verbose=False)

    args = parser.parse_args()

    if args.language_unprocessed:
        languages = args.language_unprocessed.split(",")
        args.language = [lang.strip() for lang in languages]
        for lang in languages:
            if lang not in VALID_PROGRAMMING_LANGUAGES:
                parser.error(f"Invalid language: '{lang}'")
        args.language = languages
    else:
        args.language = None

    return args


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
        handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()],
    )

    logging.info(args)

    problem_folder_name_template = Template(args.problem_folder_name)
    problem_statement_filename_template = Template(args.problem_statement_filename)
    problem_statement_template = Template(args.problem_statement_content)
    submission_filename_template = Template(args.submission_filename)

    leetcode = LeetCode()
    cookies = args.cookies

    if not cookies:
        cookies = input("Insert LeetCode cookies: ")

    if not leetcode.set_cookies(cookies):
        logging.error(
            "Cookies not valid. Copy them from the Network tab of your browser by clicking on any leetcode.com request and going in Request Headers > cookie. Check README.md file for further information"
        )
        exit(1)

    # Create output folder if it doesn't already exist
    if not os.path.exists(args.folder):
        os.mkdir(args.folder)
    os.chdir(args.folder)

    title_slug_to_problem_folder_name: dict[str, str] = dict()

    for submission in leetcode.get_submissions():
        if args.only_accepted and submission.status_display != "Accepted":
            continue

        if args.language and submission.lang not in args.language:
            continue

        if submission.title_slug not in title_slug_to_problem_folder_name:
            problem_statement = leetcode.get_problem_statement(submission.title_slug)
            problem_folder_name = problem_folder_name_template.substitute(
                **problem_statement.__dict__
            )
            title_slug_to_problem_folder_name[
                submission.title_slug
            ] = problem_folder_name
            if not os.path.exists(problem_folder_name):
                os.mkdir(problem_folder_name)
            os.chdir(problem_folder_name)

            problem_statement_filename = problem_statement_filename_template.substitute(
                **problem_statement.__dict__
            )
            if not os.path.exists(problem_statement_filename):
                with open(problem_statement_filename, "w+") as problem_statement_file:
                    problem_statement_file.write(
                        problem_statement_template.substitute(
                            **problem_statement.__dict__
                        )
                    )
        else:
            os.chdir(title_slug_to_problem_folder_name[submission.title_slug])

        submission_filename = submission_filename_template.substitute(
            **submission.__dict__
        )
        if not os.path.exists(submission_filename):
            logging.info(f"Writing {submission.title_slug}/{submission_filename}")
            sub_file = open(submission_filename, "w+")
            sub_file.write(submission.code)
            sub_file.close()
        else:
            logging.info(
                f"{submission.title_slug}/{submission_filename} already exists, skipping it"
            )

        os.chdir("..")


if __name__ == "__main__":
    main()
