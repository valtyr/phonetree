FROM alpine:3.6
EXPOSE 5000
VOLUME /usr/src/app/public
WORKDIR /usr/src/app
RUN apk add --no-cache \
    uwsgi \
    uwsgi-python3 \
    python3
COPY . .
RUN rm -rf public/*
RUN pip3 install --no-cache-dir -r requirements.txt
CMD ["uwsgi", "--socket", "0.0.0.0:5000", \
              "--plugins", "python3", \
              "--protocol", "uwsgi", \
              "--wsgi", "main:application"]