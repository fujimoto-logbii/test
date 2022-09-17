FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
WORKDIR /app
COPY /django/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY /django/code /app

CMD python manage.py runserver 0.0.0.0:8000