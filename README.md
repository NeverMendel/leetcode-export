# LeetCode Export

Python script and Docker image to export your LeetCode submissions.

## DISCLAIMER

The problems hosted on leetcode.com are intellectual propriety of LeetCode LLC unless specified otherwise. **DO NOT
UPLOAD THE DESCRIPTION OF LEETCODE PROBLEMS ON GITHUB OR ON ANY OTHER WEBSITE** or you might receive ad DMCA Takedown
notice.

Before using this script make read [LeetCode Terms of Service](https://leetcode.com/terms/).

To avoid committing the problem description on git, you can add `*.txt` to your `.gitignore` file.

## How it works

This script uses LeetCode REST and GraphQL APIs to download all your LeetCode submitted solutions.

Before running the script, make sure that python3 is installed in your system.

If you prefer, you can use the Docker image to download your submissions. For further instructions read the
section [Docker Image here](#docker-image).

## How to use

To use `leetcode-export` you can either download it from pypi.org or you can clone this repository.

### Download from pypi.org

Run `pip install leetcode-export` to install leetcode-export, you might have to use `pip3` of your system. To use the
script run `leetcode-export`, optionally supply the script arguments, for more instructions read the
section [script arguments here](#script-arguments).

### Clone the repository

Clone this repository:

```bash
git clone https://github.com/NeverMendel/leetcode-export
```

Install all the needed dependencies:

```bash
pip install -r requirements.txt
```

You can either install leetcode-export in your system or just execute it:

- To install it run:
    ```bash
    python setup.py install
    ```

- To execute the script without installing it:
    ```bash
    python -m leetcode_export --folder submissions
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

## Login

To download your submissions you need to log in your LeetCode account by providing the cookies. To log in using cookies,
you need to get them from a session where you are already logged in.

**Steps required**:

- Login in your LeetCode account in your browser
- Open the browser's Dev Tool
- Click on the Network tab
- Copy the cookie header that can be found under Request Headers in any leetcode.com request.

You can insert the cookie string that you have just copied in the interactive menu (recommended) or you can pass it as a
program argument when lunching the script, like in the following example:

```bash
python leetcode-export --cookies {COOKIES}
```

## Script arguments

The script accepts the following arguments:

```
usage: leetcode-export [-h] [--cookies COOKIES] [--folder FOLDER]
                       [--problem-filename PROBLEM_FILENAME]
                       [--submission-filename SUBMISSION_FILENAME] [-v] [-vv]
                       [-V]

Export LeetCode solutions

optional arguments:
  -h, --help            show this help message and exit
  --cookies COOKIES     set LeetCode cookies
  --folder FOLDER       set output folder
  --problem-filename PROBLEM_FILENAME
                        problem description filename format
  --submission-filename SUBMISSION_FILENAME
                        submission filename format
  -v, --verbose         enable verbose logging details
  -vv, --extra-verbose  enable more verbose logging details
  -V, --version         show program's version number and exit
```

Using the interactive menu is preferred as it will avoid storing your cookies in the command history.

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
question_id: int
difficulty: str
stats: str
title: str
title_slug: str
```

Default problem description filename template: `${question_id} - ${title_slug}.txt`

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

[MIT License](LICENSE)