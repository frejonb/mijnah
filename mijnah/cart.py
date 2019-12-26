import requests
from .product import Product

MEMBER_URL = 'https://www.ah.nl/common/api/member/v1'
CART_URL = 'https://www.ah.nl/common/api/basket/v2'
CART_SERVICE_URL = 'https://www.ah.nl/service/rest/shoppinglists/0/items'


class Cart:
    def __init__(self, ah_token=None):
        self._session = requests.Session()
        if not ah_token:
            raise Exception('Please fill in auth tokens')
        self._session.headers.update({
            'content-type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/73.0.3683.103 Safari/537.36',
            'cache-control': 'no-cache',
            'cookie': 'ah_token=' + ah_token
        })
        resp = requests.get(MEMBER_URL, headers=self._session.headers)
        resp_json = resp.json()
        if resp.status_code != 200 or (
             'status' in resp_json and resp_json['status'] == 'anonymous'):
            raise Exception('Incorrect authentication: '+repr(resp_json))

    def list_cart(self):
        resp = requests.get(CART_URL, headers=self._session.headers)
        if resp.status_code != 200:
            raise Exception(
                'Error while getting shopping cart: '+repr(resp.json()))
        resp_json = resp.json()
        return [{
            'quantity': item['quantity'],
            'product': Product(str(item['id']))
            } for item in resp_json['products']]

    def add_to_cart(self, product_id, amount=1):
        product = {
            "items": [{
                "id": product_id,
                "quantity": amount
            }]
        }
        resp = requests.post(CART_URL+'/add',
                             headers=self._session.headers,
                             json=product)
        resp_json = resp.json()
        if resp.status_code != 200 or (
                'failed' in resp_json and len(resp_json['failed']) > 0):
            raise Exception(
                'Couldn\'t add to cart: '+repr(resp_json['failed']))

    def update_cart(self, product_id, amount):
        payload = {
            "items": [{
                "id": product_id,
                "quantity": amount
            }]
        }
        resp = requests.post(CART_URL+'/update',
                             headers=self._session.headers,
                             json=payload)
        if resp.status_code != 200:
            raise Exception('Error while updating cart: '+repr(resp.json()))

    def empty_cart(self):
        resp = requests.delete(CART_SERVICE_URL, headers=self._session.headers)
        if resp.status_code != 200:
            raise Exception('Error while emptying cart: '+repr(resp.json()))
