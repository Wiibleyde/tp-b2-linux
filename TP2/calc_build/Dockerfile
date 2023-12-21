FROM python:3.12
WORKDIR /app

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

COPY calc.py .
COPY src/logs.py ./src/

RUN mkdir -p /app/logs/

# Expose the port of the environment variable or 13337 by default
EXPOSE ${CALC_PORT:-13337}

CMD ["python", "calc.py"]