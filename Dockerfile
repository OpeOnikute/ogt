FROM python:2.7-alpine

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/

EXPOSE 8000 443

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000"]

