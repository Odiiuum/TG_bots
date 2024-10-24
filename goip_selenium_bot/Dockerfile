FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    chromium-driver \
    chromium

RUN pip install -r requirements.txt

COPY . .

CMD ["bash", "-c", "python bot.py & python app.py"]
