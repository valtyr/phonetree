FROM tiangolo/uwsgi-nginx-flask:python3.6

COPY ./app /app
RUN pip install -r requirements.txt

EXPOSE 8037:80
