FROM python:3.12-alpine

RUN apk add curl postgresql-dev

WORKDIR /app/

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

CMD ["sh", "entrypoint.sh"]
