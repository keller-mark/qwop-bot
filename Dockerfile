FROM python:3.6-alpine

WORKDIR /usr/src/app

RUN apk add --no-cache gcc musl-dev
RUN pip install gym
RUN echo "http://dl-4.alpinelinux.org/alpine/v3.4/main" >> /etc/apk/repositories && \
	echo "http://dl-4.alpinelinux.org/alpine/v3.4/community" >> /etc/apk/repositories


RUN apk update && \
	apk add python py-pip curl unzip libexif udev chromium chromium-chromedriver xvfb && \
	pip install selenium && \
	pip install pyvirtualdisplay

RUN apk add curl unzip libexif udev chromium chromium-chromedriver xvfb


COPY . .

CMD [ "tail", "-f", "/dev/null" ]


