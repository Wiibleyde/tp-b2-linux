FROM python:3.12
WORKDIR /app

# COPY requirements.txt .
# RUN python3 -m pip install -r requirements.txt
RUN pip install websockets
RUN pip install motor

COPY chat.py .
COPY src/logs.py ./src/

RUN mkdir -p /app/logs/

# Expose the port of the environment variable or 13337 by default
EXPOSE ${CHAT_PORT:-13337}

CMD ["python", "chat.py"]