FROM python:3.6.12-alpine3.12

COPY main.py main.py
COPY summary.py summary.py
COPY requirements.txt requirements.txt
COPY crontab crontab

RUN pip install -r requirements.txt

RUN crontab crontab

ENV DB_USER=${DB_USER}
ENV DB_PASS=${DB_PASS}
ENV DB_NAME=${DB_NAME}

CMD ["crond", "-f"]
