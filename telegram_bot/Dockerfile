FROM python:3.12-slim

WORKDIR /app

RUN pip install aiogram pydantic_settings

COPY . /app

CMD ["python3", "main.py"]
