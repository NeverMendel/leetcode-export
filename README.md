# LeetCode Export

Python script and Docker image to export your LeetCode submissions.

If you find LeetCode Export helpful, please consider giving it a star ⭐️. Your support helps me gauge its usage and motivates further development.

## 📝 Table of Contents

- [DISCLAIMER](#DISCLAIMER)
- [About](#about)
- [Getting started](#getting-started)
- [Script arguments](#script-arguments)
- [Special mentions](#special-mentions)
- [License](#license)

## ⚠️ DISCLAIMER <a name="disclaimer"></a>

The problems hosted on leetcode.com are intellectual propriety of LeetCode LLC unless specified otherwise. **DO NOT
UPLOAD THE DESCRIPTION OF LEETCODE PROBLEMS ON GITHUB OR ON ANY OTHER WEBSITE** or you might receive ad DMCA Takedown
notice.

Before using this script read the [LeetCode Terms of Service](https://leetcode.com/terms/).

## ⚙️ About <a name="about"></a>

This script uses LeetCode REST and GraphQL APIs to download all your LeetCode submitted solutions.

Before running the script, make sure that python3 is installed in your system.

If you prefer, you can use the Docker image to download LeetCode submissions. For more information read the
section [Docker Image](#docker-image).

### ✨ New Features Added
- **API Resilience**: Added retry logic with exponential backoff for GraphQL queries and submission requests to prevent crashes on network timeouts or rate limits.
- **Topic Tags Export**: Problems now extract and expose `topicTags` for categorizing solutions by LeetCode topics.

## 🏁 Getting started <a name="getting-started"></a>

### Download `leetcode-export`

To use `leetcode-export` download it from pypi.org, pull the docker image, or clone this repository.

#### Download from pypi.org

Run `pip install leetcode-export` to install leetcode-export, you might have to use `pip3` of your system. Then execute
run the script `leetcode-export`, optionally supply the script arguments. For more information read the
section [script arguments](#script-arguments).

#### Docker Image

Download the docker image from DockerHub:

```bash
docker pull nevermendel/leetcode-export
```

Download all your LeetCode submission in the current folder:

```bash
docker run -it -v $(pwd):/usr/app/out --rm nevermendel/leetcode-export
```

#### Clone the repository

Clone this repository:

```bash
git clone https://github.com/NeverMendel/leetcode-export
```

Install all the needed dependencies:

```bash
pip install -r requirements.txt
```

Install leetcode-export in your system or just execute it:

- To install the script:
    ```bash
    pip install .
    ```

- To execute the script without installing it:
    ```bash
    python -m leetcode_export --folder submissions
    ```

### Login

`leetcode-export` requires a valid LeetCode account to download its submissions. Login to your LeetCode account by
providing the cookies. To log in using cookies, get them from an existing session.

**Steps required**:

- Login in to LeetCode in the web browser
- Open the browser's Dev Tool
- Click on the Network tab
- Copy the cookie header that can be found under Request Headers in any leetcode.com request.

You can insert the cookie string that you have just copied in the interactive menu (recommended) or you can pass it as a
program argument when lunching the script, like in the following example:

```bash
python leetcode-export --cookies {COOKIES}
```

Using the interactive menu is preferred because it will avoid storing cookies in the command history.

## Script arguments

The script accepts the following arguments:

```
usage: leetcode-export [-h] [--cookies COOKIES] [--folder FOLDER]
                       [--problem-folder-name PROBLEM_FOLDER_NAME]
                       [--no-problem-statement]
                       [--problem-statement-filename PROBLEM_STATEMENT_FILENAME]
                       [--problem-statement-content PROBLEM_STATEMENT_CONTENT]
                       [--submission-filename SUBMISSION_FILENAME]
                       [--only-accepted] [--only-last-submission]
                       [--language LANGUAGE_UNPROCESSED] [-v] [-vv] [-V]

Export LeetCode submissions

options:
  -h, --help            show this help message and exit
  --cookies COOKIES     set LeetCode cookies
  --folder FOLDER       set output folder
  --problem-folder-name PROBLEM_FOLDER_NAME
                        problem folder name format
  --no-problem-statement
                        do not save problem statement
  --problem-statement-filename PROBLEM_STATEMENT_FILENAME
                        problem statement filename format
  --problem-statement-content PROBLEM_STATEMENT_CONTENT
                        problem statement content format
  --submission-filename SUBMISSION_FILENAME
                        submission filename format
  --only-accepted       save accepted submissions only
  --only-last-submission
                        only save the last submission for each programming language
  --language LANGUAGE_UNPROCESSED
                        save submissions for specified programming languages.
                        syntax: --language=<lang1>,<lang2>,...
                        languages: python, python3, c, cpp, csharp, java,
                                   kotlin, mysql, mssql, oraclesql, javascript,
                                   html, php, golang, scala, pythonml,
                                   rust, ruby, bash, swift
                        example: --language=python,cpp,java
  -v, --verbose         enable verbose logging details
  -vv, --extra-verbose  enable more verbose logging details
  -V, --version         show program's version number and exit
```

### Problem template arguments

#### Problem statement filename template

To change the format of the problem statement filename provide a template as a string when executing the
script.

```bash
python leetcode-export --problem-statement-filename PROBLEM_STATEMENT_FILENAME
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

Default problem statement filename template: `${question_id} - ${title_slug}.html`

#### Problem statement content template

To change the format of the problem statement content provide a template as a string when executing the
script.

```bash
python leetcode-export --problem-statement-content PROBLEM_STATEMENT_CONTENT
```

The template can contain parameters that will later be replaced based on the LeetCode problem information. The available
parameters are the ones contained in [problem statement filename template](#problem-statement-filename-template) plus:

```python
content: str
```

Default problem statement content template:
`<h1>${question_id} - ${title}</h1><h2>Difficulty: ${difficulty} - <a href="https://leetcode.com/problems/${title_slug}/">${title_slug}</a></h2>${content}`

#### Submission filename template

To change the format of the submission filename, you can provide a template as a string when lunching the script.

```bash
python leetcode-export --submission-filename SUBMISSION_FILENAME
```

The template can contain parameters that will later be replaced based on the submission information. The available
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


## 🚀 Full Automation: Daily GitHub Sync

You can fully automate your LeetCode backup to a separate GitHub repository using **GitHub Actions** and the provided **Chrome Extension**.

### 1. Create your Solutions Repository
1. Create a new private GitHub repository (e.g., `LeetCode-Solutions`).
2. Create a file `.github/workflows/sync.yml` with the following content:

```yaml
name: Daily LeetCode Sync
on:
  schedule:
    - cron: "0 */8 * * *"
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.10"
      - run: |
          pip install git+https://github.com/MohamedMousad/leetcode-export.git@feature/api-retry-and-tags
      - env:
          LEETCODE_COOKIE: ${{ secrets.LEETCODE_COOKIE }}
        run: |
          python -m leetcode_export --folder .
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
          git add .
          git commit -m "Auto-sync: Daily update" || echo "No changes"
          git push origin main
```

### 2. Set Up the Chrome Extension
Because LeetCode cookies change, we provide a Chrome Extension that automatically syncs your active session cookie to your GitHub repository securely as a secret.
1. Generate a **GitHub Personal Access Token (Classic)** with `repo` and `workflow` permissions.
2. Open Chrome and navigate to `chrome://extensions/`.
3. Enable **Developer mode** (top right corner).
4. Click **Load unpacked** and select the `chrome-extension` folder found in this repository.
5. Click the extension icon in your browser toolbar, paste your PAT and repository name (e.g., `YourUser/LeetCode-Solutions`), and click **Save**.
6. Whenever you log into LeetCode, click **Push Cookie to GitHub Now** in the extension to automatically securely update the `LEETCODE_COOKIE` secret in your repository. 

Your GitHub action will now run seamlessly every day!

## Special mentions

Thanks to [skygragon](https://github.com/skygragon) for
developing [leetcode-cli](https://github.com/skygragon/leetcode-cli), which I used as documentation for LeetCode APIs.
The license of leetcode-cli is available [here](https://github.com/skygragon/leetcode-cli/blob/master/LICENSE).

## License

[MIT License](LICENSE)
