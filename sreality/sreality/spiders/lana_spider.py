import scrapy

from sreality.items import SrealityItem


class LanaSpiderSpider(scrapy.Spider):
    name = "lana_spider"
    allowed_domains = ["sreality.cz"]
    start_urls = [
        'https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&sort=0&per_page=' + str(
            100) + '&page=' + str(x) + '' for x in range(1, 6)]

    def parse(self, response):
        jsonresponse = response.json()
        for item in jsonresponse["_embedded"]['estates']:
            yield scrapy.Request('https://www.sreality.cz/api' + item['_links']['self']['href'],
                                 callback=self.parse_estate)


    def parse_estate(self, response):
        jsonresponse = response.json()
        estate = SrealityItem()
        estate['title'] = jsonresponse['name']['value']
        # item["ADDRESS"] = jsonresponse['locality']['value']

        for images in jsonresponse['_embedded']['images']:
            if images['_links']['dynamicDown']:
                tmp = images['_links']['dynamicDown']['href'].replace('{width}', '400')
                tmp = tmp.replace('{height}', '300')
                estate['image_urls'] = tmp
                break

        yield estate
