FROM python:3.11

WORKDIR /app

COPY server.py /app
COPY requirements.txt /app

RUN pip install -r requirements.txt

#RUN pip install pyjwt

EXPOSE 5000

CMD ["python", "server.py"]
