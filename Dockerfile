FROM python:3.8.6

WORKDIR . .

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential


COPY requirements.txt .

RUN pip install -r requirements.txt

ENV FLASK_APP=main.py

COPY . .

EXPOSE 80

CMD ["python", "main.py"]