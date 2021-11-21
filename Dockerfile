FROM python:3.8.6

WORKDIR .

RUN apt-get update
RUN python -m pip install --upgrade pip
RUN pip install python-dotenv

COPY requirements.txt .

RUN pip install -r requirements.txt

ENV FLASK_APP=wsgi.py

COPY . .

CMD ["flask", "run"]