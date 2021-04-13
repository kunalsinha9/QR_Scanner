
FROM python:3.7-slim-buster
COPY . /app
WORKDIR /app
RUN apt-get update
RUN apt-get install -y python-zbar libzbar-dev python-qrtools
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip3 install -r requirements.txt

EXPOSE 8000

CMD [ "gunicorn", "app:app" , "--bind", "0.0.0.0:8000"]