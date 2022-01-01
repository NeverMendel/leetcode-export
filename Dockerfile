FROM alpine:latest

RUN apk add --no-cache \
      nss \
      ca-certificates \
      python3 \
      py3-pip

# Copy current directory to /usr/src/app
ADD . /usr/src/app
WORKDIR /usr/src/app

# Create out folder
RUN mkdir -p out

# Install leetcode-export
python3 ./setup.py install

ENTRYPOINT ["leetcode-export", "--folder", "out"]