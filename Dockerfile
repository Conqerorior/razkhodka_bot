FROM python:3.9-alpine

WORKDIR /razkhodka_bot

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "main.py"]