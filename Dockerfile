# Pull base image
FROM python:3.10.2-slim-bullseye

ENV PYTHONUNBUFFERED=1
RUN apt clean && apt update && apt install curl -y

# Set work directory
WORKDIR /instagram

# Install dependencies
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt

# Copy project
COPY . .
CMD python3 manage.py runserver 0.0.0.0:8000