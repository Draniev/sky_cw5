FROM python:3.11-slim

WORKDIR /home/app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD flask --app run.py run -h 0.0.0.0 -p 8080

