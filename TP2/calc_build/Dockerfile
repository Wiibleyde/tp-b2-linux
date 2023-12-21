FROM python:3.12
WORKDIR /app

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

COPY main.py .
COPY src/logs.py ./src/

RUN mkdir -p /app/logs/

EXPOSE 13337

CMD ["python", "main.py", "-p", "13337"]