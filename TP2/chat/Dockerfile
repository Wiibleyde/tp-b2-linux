FROM python:3.12
WORKDIR /app

RUN pip install websockets
RUN pip install motor
RUN pip install redis

COPY chat.py .
COPY src/logs.py ./src/

RUN mkdir -p /app/logs/

# Expose the port of the environment variable or 13337 by default
EXPOSE ${CHAT_PORT:-13337}

CMD ["python", "chat.py"]