"""
LeetCode Export.

Export your LeetCode submissions and related problem statements.
"""

import argparse
import logging
import os
from string import Template
from typing import Optional, Set

from leetcode_export._version import __version__
from leetcode_export.leetcode import LeetCode
from leetcode_export.utils import VALID_PROGRAMMING_LANGUAGES


def parse_args():
    parser = argparse.ArgumentParser(
        description="Export LeetCode submissions",
        formatter_class=lambda prog: argparse.RawTextHelpFormatter(
            "leetcode-export", width=80
        ),
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
        "--no-problem-statement",
        dest="no_problem_statement",
        action="store_true",
        help="do not save problem statement",
    )
    parser.add_argument(
        "--problem-statement-filename",
        type=str,
        default="${question_id}-${title_slug}.md",
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
        "--only-last-submission",
        dest="only_last_submission",
        action="store_true",
        help="only save the last submission for each programming language",
    )
    parser.add_argument(
        "--language",
        dest="language_unprocessed",
        type=str,
        help="save submissions for specified programming languages.\n"
        "syntax: --language=<lang1>,<lang2>,...\n"
        "languages: python, python3, pythondata, c, cpp,\n"
        "           csharp, java, kotlin, mysql, mssql,\n"
        "           oraclesql, javascript, html, php, golang,\n"
        "           scala, pythonml, rust, ruby, bash, swift,\n"
        "           typescript, elixir, erlang, racket, dart\n"
        "example: --language=python,cpp,java",
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
        "--checkpoint-file",
        type=str,
        help="path to checkpoint file for incremental backups (stores Unix timestamp of newest processed submission)",
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


def load_checkpoint(checkpoint_file: str) -> Optional[int]:
    """
    Load timestamp from checkpoint file
    :param checkpoint_file: path to checkpoint file
    :return: Unix timestamp or None if file doesn't exist or is invalid
    """
    if not os.path.exists(checkpoint_file):
        logging.info(f"Checkpoint file {checkpoint_file} does not exist")
        response = input(f"Create checkpoint file at {checkpoint_file} and start from beginning? (y/N): ")
        if response.lower() in ['y', 'yes']:
            write_checkpoint(checkpoint_file, 0)
            return 0
        else:
            logging.error("Checkpoint file required for incremental backup. Exiting.")
            exit(1)
    try:
        with open(checkpoint_file, 'r') as f:
            timestamp = int(f.read().strip())
            logging.info(f"Loaded checkpoint timestamp: {timestamp}")
            return timestamp
    except (ValueError, IOError) as e:
        logging.error(f"Failed to read checkpoint file {checkpoint_file}: {e}")
        exit(1)


def write_checkpoint(checkpoint_file: str, timestamp: int) -> None:
    """
    Write timestamp to checkpoint file
    :param checkpoint_file: path to checkpoint file
    :param timestamp: Unix timestamp to write
    """
    try:
        with open(checkpoint_file, 'w') as f:
            f.write(str(timestamp))
        logging.debug(f"Updated checkpoint to timestamp: {timestamp}")
    except IOError as e:
        logging.error(f"Failed to write checkpoint file {checkpoint_file}: {e}")


def configure_logging(args):
    logging_file_handler = logging.FileHandler("debug.log", encoding="UTF8")
    logging_file_handler.setLevel(logging.DEBUG)

    logging_stream_handler = logging.StreamHandler()

    # Set stream logging level based on program arguments
    logging_stream_handler.setLevel(logging.WARNING)
    if args.verbose:
        logging_stream_handler.setLevel(logging.INFO)
    if args.extra_verbose:
        logging_stream_handler.setLevel(logging.DEBUG)

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s",
        handlers=[logging_file_handler, logging_stream_handler],
    )


def main():
    args = parse_args()
    configure_logging(args)

    logging.info("leetcode-export run with arguments: " + str(args))

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
            "Cookies not valid. Copy them from the Network tab of your browser by clicking on any leetcode.com request and going in Request Headers > cookie. Check README.md file for more information"
        )
        exit(1)

    # Create output folder if it doesn't already exist
    if not os.path.exists(args.folder):
        logging.info("Output folder not found, creating it")
        os.mkdir(args.folder)
    os.chdir(args.folder)
    base_folder = os.getcwd()

    title_slug_to_problem_folder_name: dict[str, str] = dict()
    title_slug_to_exported_languages: dict[str, set[str]] = dict()

    last_submission_timestamp: Optional[int] = None

    # Handle checkpoint functionality
    checkpoint_timestamp: Optional[int] = None
    newest_processed_timestamp: Optional[int] = None
    submissions_processed = 0

    if args.checkpoint_file:
        checkpoint_timestamp = load_checkpoint(args.checkpoint_file)
        logging.info(f"Using checkpoint file: {args.checkpoint_file}")
        if checkpoint_timestamp > 0:
            logging.info(f"Only processing submissions newer than timestamp {checkpoint_timestamp}")

    print("Exporting LeetCode submissions...")

    for submission in leetcode.get_submissions(since_timestamp=checkpoint_timestamp):
        if (
            last_submission_timestamp is not None
            and submission.timestamp > last_submission_timestamp
        ):
            logging.warning(
                "Submissions are not in reverse chronological order, --only-last-submission flag might not work as expected if used. Please report this issue on GitHub attaching the debug.log file: https://github.com/NeverMendel/leetcode-export/issues"
            )
        last_submission_timestamp = submission.timestamp

        if args.only_accepted and submission.status_display != "Accepted":
            logging.info(
                f"Skipping {submission.title_slug} {submission.date_formatted} because its status is '{submission.status_display}'"
            )
            continue

        if args.language and submission.lang not in args.language:
            logging.info(
                f"Skipping {submission.title_slug} {submission.date_formatted} because its programming language is {submission.lang}"
            )
            continue

        if submission.title_slug not in title_slug_to_exported_languages:
            title_slug_to_exported_languages[submission.title_slug] = set()

        if (
            args.only_last_submission
            and submission.title_slug in title_slug_to_exported_languages
            and submission.lang
            in title_slug_to_exported_languages[submission.title_slug]
        ):
            logging.info(
                f"Skipping {submission.title_slug} {submission.date_formatted} in {submission.lang} because a more recent submission has already been exported"
            )
            continue
        title_slug_to_exported_languages[submission.title_slug].add(submission.lang)

        if submission.title_slug not in title_slug_to_problem_folder_name:
            problem_statement = leetcode.get_problem_statement(submission.title_slug)
            problem_folder_name = problem_folder_name_template.substitute(
                **problem_statement.__dict__
            )
            title_slug_to_problem_folder_name[submission.title_slug] = (
                problem_folder_name
            )
            if not os.path.exists(problem_folder_name):
                os.makedirs(problem_folder_name, exist_ok=True)
            os.chdir(problem_folder_name)

            problem_statement_filename = problem_statement_filename_template.substitute(
                **problem_statement.__dict__
            )
            if not args.no_problem_statement and not os.path.exists(
                problem_statement_filename
            ):
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
        submission_was_written = False
        if not os.path.exists(submission_filename):
            logging.info(f"Writing {submission.title_slug}/{submission_filename}")
            sub_file = open(submission_filename, "w+")
            sub_file.write(submission.code)
            sub_file.close()
            submission_was_written = True
        else:
            logging.info(
                f"{submission.title_slug}/{submission_filename} already exists, skipping it"
            )

        # Track processing for checkpoint updates
        if submission_was_written:
            submissions_processed += 1
            if newest_processed_timestamp is None or submission.timestamp > newest_processed_timestamp:
                newest_processed_timestamp = submission.timestamp

        os.chdir(base_folder)

    # Final summary and checkpoint update
    if args.checkpoint_file:
        if submissions_processed > 0:
            # Only update checkpoint after successful completion of all processing
            write_checkpoint(args.checkpoint_file, newest_processed_timestamp)
            print(f"Processed {submissions_processed} new submissions")
            print(f"Updated checkpoint to timestamp: {newest_processed_timestamp}")
        else:
            logging.info("No new submissions found since last checkpoint")


if __name__ == "__main__":
    main()
