FROM python:3.10-slim

WORKDIR /netskope-url-deploy

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

WORKDIR /netskope-url-deploy/app

ENTRYPOINT [ "python" ]

CMD [ "main.py" ]