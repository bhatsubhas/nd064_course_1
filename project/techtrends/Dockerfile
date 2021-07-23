FROM python:3.9-alpine

RUN mkdir /app

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt && \
    python init_db.py

EXPOSE 3111

CMD ["python", "app.py"]