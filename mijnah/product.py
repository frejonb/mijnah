import requests

PRODUCT_URL = 'https://www.ah.nl/zoeken/api/products/product?webshopId='


class Product:
    def __init__(self, product_id=None):
        if not id:
            raise Exception("Product id is empty")
        resp = requests.get(PRODUCT_URL+product_id)
        if resp.status_code != 200:
            raise Exception('Error while getting product: '+repr(resp))
        resp_json = resp.json()
        self._product = resp_json['card']['products'][0]

    @property
    def id(self):
        return self._product['id']

    @property
    def category(self):
        return self._product['category']

    @property
    def description(self):
        return self._product['summary']

    @property
    def brand(self):
        return self._product['brand']

    @property
    def price(self):
        return self._product['price']['now']

    @property
    def name(self):
        return self._product['title']

    def __repr__(self):
        return repr(self.name)
