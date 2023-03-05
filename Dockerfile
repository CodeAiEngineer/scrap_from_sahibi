FROM python:3.8

ADD main.py .
ADD filtre.ini .


RUN pip install beautifulsoup4
RUN pip install Flask
RUN pip install Flask-Mail
RUN pip install urllib3
RUN pip install configparser


CMD [ "python", "./main.py" ]




