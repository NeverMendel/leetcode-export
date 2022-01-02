FROM alpine:latest

RUN apk add --no-cache \
      nss \
      ca-certificates \
      python3 \
      py3-pip

# Copy current directory to /usr/src/app
ADD . /usr/app
WORKDIR /usr/app

# Create out folder
RUN mkdir -p out

# Install leetcode-export
python3 ./setup.py install

ENTRYPOINT ["leetcode-export", "--folder", "out"]