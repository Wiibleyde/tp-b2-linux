FROM python:3.12
WORKDIR /app

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

COPY monit.py .
COPY monit-api.py .
COPY config.json .

RUN mkdir -p /var/monit

# Expose the port of the environment variable or 13337 by default
EXPOSE 5000

CMD ["python", "monit-api.py"]