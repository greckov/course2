FROM python:3.9-slim-buster
WORKDIR /course2
ENV PYTHONUNBUFFERED=True
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . ./
