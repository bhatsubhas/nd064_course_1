FROM python:alpine

LABEL author="Subhas Bhat <bhatsubhas@gmail.com>"

ADD . .

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "app.py"]