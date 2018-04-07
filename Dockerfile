FROM python:3.6-alpine

WORKDIR /usr/src/app

RUN apk add --no-cache gcc musl-dev

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#CMD [ "python", "./app.py" ]

