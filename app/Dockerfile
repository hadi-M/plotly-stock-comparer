# pull official base image
FROM python:3.8-slim-buster

# set working directory
WORKDIR /usr/src/app

# install python dependencies
RUN python -m pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
# RUN apt update
# RUN apt install -y gunicorn
# CMD ["python", "main.py"]
# CMD ["ls"]
# CMD ["gunicorn", "app.main:server", "-b", ":8050"]
# RUN gunicorn app.main:server -b :8050