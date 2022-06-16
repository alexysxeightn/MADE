FROM python:3.6-slim-stretch

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache -r requirements.txt

COPY . .

ENTRYPOINT [ "python", "predict.py" ]
