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

# Install dependencies
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "./main.py", "--folder", "out"]