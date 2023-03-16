FROM python:alpine3.17
WORKDIR /usr/src/sreality

RUN apk add --no-cache gcc musl-dev linux-headers libpq-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000

COPY ./sreality ./sreality
COPY scrapy.cfg scrapy.cfg
CMD ["scrapy", "crawl", "lana_spider"]