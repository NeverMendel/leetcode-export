# LeetCode Export

> Python script and Docker image to export your LeetCode solutions

## DISCLAIMER

All the problems hosted on leetcode.com are intellectual propriety of LeetCode, LLC. **DO NOT UPLOAD
THE DESCRIPTION OF LEETCODE PROBLEMS ON GITHUB OR ON ANY OTHER WEBSITE** or you might receive ad DMCA Takedown notice.

Read [LeetCode Terms of Service here](https://leetcode.com/terms/).

To avoid committing the problem description on git, you can add `*.txt` to your `.gitignore` file.

## How it works

This script uses `selenium` and LeetCode APIs to download all your LeetCode submitted solutions.

Before running the script, make sure that python3, chrome and `chromedriver` are installed in your system.

If you do not want to configure and install all the required dependencies, you can download the Docker image. For
further instructions read the section [Docker Image here](#docker-image).

`chromedriver` is used to get the cookies needed to download your LeetCode submissions. Alternatively, you can provide
the cookies using the flag `--cookies` in the Python script.

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

## License

[Apache License 2.0](LICENSE)