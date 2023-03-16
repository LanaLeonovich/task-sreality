FROM python:alpine3.17
WORKDIR /usr/src/server

RUN apk add --no-cache gcc musl-dev linux-headers libpq-dev
EXPOSE 8080

COPY server.py server.py
CMD ["python", "./server.py"]