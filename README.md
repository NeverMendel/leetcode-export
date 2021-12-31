# LeetCode Export

> Python script and Docker image to export your LeetCode solutions

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

To use the Docker Image you first need to download it from the Docker repository by running:

```bash
docker pull nevermendel/leetcode-export
```

Now you can download all your LeetCode submission in the current folder by executing:

```bash
docker run -it -v $(pwd):/usr/app/out --rm nevermendel/leetcode-export
```

## App parameters

The script accepts the following parameters:

```bash
usage: app.py [-h] [--username USERNAME] [--password PASSWORD]
              [--folder FOLDER] [--cookies COOKIES] [-v] [-vv]

Export LeetCode solutions

optional arguments:
  -h, --help            show this help message and exit
  --username USERNAME   LeetCode username
  --password PASSWORD   LeetCode password
  --folder FOLDER       Output folder
  --cookies COOKIES     LeetCode cookies
  -v, --verbose         Enable verbose logging details
  -vv, --extra-verbose  Enable more verbose logging details
```

## Login

There are two ways to login in your LeetCode account, by providing username and password or by passing the cookies as
program argument.

### Username and Password

To login using username and password, insert them when prompted or pass them as parameter when lunching the script, like
in the following example:

```bash
python ./app.py --username {USERNAME} --password {PASSWORD}`
```

The former option is to be preferred as it will avoid storing your password in the command history.

### Cookies

To login using cookies, pass the string containing them as parameter when lunching the script, like in the following
example:

```bash
python ./app.py --cookies {COOKIES}
```

## Special mentions

Thanks to [skygragon](https://github.com/skygragon) for
developing [leetcode-cli](https://github.com/skygragon/leetcode-cli), which I used as documentation for LeetCode APIs.
The license of leetcode-cli is available [here](https://github.com/skygragon/leetcode-cli/blob/master/LICENSE).

## License

[Apache License 2.0](LICENSE)