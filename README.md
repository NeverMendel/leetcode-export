# LeetCode Export

Python script and Docker image to export your LeetCode solutions.

## DISCLAIMER

All the problems hosted on leetcode.com are intellectual propriety of LeetCode, LLC. **DO NOT UPLOAD THE DESCRIPTION OF
LEETCODE PROBLEMS ON GITHUB OR ON ANY OTHER WEBSITE** or you might receive ad DMCA Takedown notice.

Before using this script make read [LeetCode Terms of Service](https://leetcode.com/terms/).

To avoid committing the problem description on git, you can add `*.txt` to your `.gitignore` file.

## How it works

This script uses LeetCode REST and GraphQL APIs to download all your LeetCode submitted solutions.

Before running the script, make sure that python3 is installed in your system.

If you prefer, you can use the Docker image to download your submissions. For further instructions read the
section [Docker Image here](#docker-image).

## How to use

### Run locally

First install all the needed dependencies by executing:

```bash
pip install -r requirements.txt
```

### Docker Image

Download the docker image from the DockerHub repository:

```bash
docker pull nevermendel/leetcode-export
```

Download all your LeetCode submission in the current folder:

```bash
docker run -it -v $(pwd):/usr/app/out --rm nevermendel/leetcode-export
```

## Script arguments

The script accepts the following arguments:

```bash
usage: leetcode-export [-h] [--username USERNAME] [--password PASSWORD]
                       [--folder FOLDER] [--cookies COOKIES] [-v] [-vv]
                       [--problem-filename PROBLEM_FILENAME]
                       [--submission-filename SUBMISSION_FILENAME]

Export LeetCode solutions

optional arguments:
  -h, --help            show this help message and exit
  --username USERNAME   Set LeetCode username
  --password PASSWORD   Set LeetCode password
  --folder FOLDER       Output folder
  --cookies COOKIES     Set LeetCode cookies
  -v, --verbose         Enable verbose logging details
  -vv, --extra-verbose  Enable more verbose logging details
  --problem-filename PROBLEM_FILENAME
                        Problem description filename format
  --submission-filename SUBMISSION_FILENAME
                        Submission filename format
```

## Login

To download your submissions you need to log in your LeetCode account. There are two ways to log in, by
username/password or by cookies.

You can either use the interactive menu to supply the required information or you can pass them as program arguments
when lunching the script.

### Username/Password

To log in using username and password, insert them using the interactive menu (preferred) or pass them as arguments when
lunching the script, like in the following example:

```bash
python leetcode-export --username {USERNAME} --password {PASSWORD}`
```

The former option is to be preferred as it will avoid storing your password in the command history.

### Cookies

To log in using cookies, pass the string containing them as arguments when lunching the script, like in the following
example:

```bash
python leetcode-export --cookies {COOKIES}
```

## Filename template arguments

### Problem description filename template

To change the format of the problem description filename, you can provide a template as a string when lunching the
script.

```bash
python leetcode-export --problem-filename PROBLEM_FILENAME
```

The template can contain parameters that will later be replaced based on the LeetCode problem information. The available
parameters are the following:

```python
questionId: int
difficulty: str
stats: str
title: str
titleSlug: str
```

Default problem description filename template: `${questionId} - ${titleSlug}.txt`

### Submission filename template

To change the format of the submission filename, you can provide a template as a string when lunching the script.

```bash
python leetcode-export --submission-filename SUBMISSION_FILENAME
```

The template can contain parameters that will later be replaced based on your submission information. The available
parameters are the following:

```python
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
```

Default submission filename
template: `${date_formatted} - ${status_display} - runtime ${runtime} - memory ${memory}.${extension}`

## Special mentions

Thanks to [skygragon](https://github.com/skygragon) for
developing [leetcode-cli](https://github.com/skygragon/leetcode-cli), which I used as documentation for LeetCode APIs.
The license of leetcode-cli is available [here](https://github.com/skygragon/leetcode-cli/blob/master/LICENSE).

## License

[Apache License 2.0](LICENSE)