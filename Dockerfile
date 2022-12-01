FROM python:3.10-alpine3.16

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY ./flaskr/ .
# COPY ./yfp-app/ .

EXPOSE 6048

CMD ["flask","run","--host","0.0.0.0","--port","6048"]