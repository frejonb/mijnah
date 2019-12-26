# mijnah
Interact with mijn Albert Heijn V2 API

# Installation
```
pip install mijnah
```

# Usage
## Cart
AH uses a recaptcha token to authenticate, so it's easier to pass a `ah_token` (found in a cookie after authenticating).

- Authentication:
  ```python
  import mijnah
  ah = mijnah.Cart(ah_token="my-ah-token")
  ```

- List cart:
  ```python
  ah.list_cart()
  ```

- Add item to cart:
  ```python
  ah.add_to_cart(product_id=1234, amount=2)
  ```
  The id can be found in the product url. For example the id in `https://www.ah.nl/producten/product/wi471282/chatelain-notre-dame-medoc` is `471282`.

- Update cart:
  ```python
  ah.update_cart(product_id=1234, amount=0)
  ```

- Empty cart:
  ```python
  ah.empty_cart()
  ```

## Product
- Initialize:
  ```python
  import mijnah
  p = mijnah.Product(product_id=1234)
  ```
- Object properties:
  ```python
  p.id
  p.name
  p.category
  p.description
  p.brand
  p.price
  ```

# Example
Getting cart totals
```python
import mijnah
import json
ah = mijnah.Cart(ah_token='ah_token')
ah.empty_cart()
# add some items
ah.add_to_cart(product_id=168153, amount=2)
ah.add_to_cart(product_id=224710, amount=1)
ah.add_to_cart(product_id=129138, amount=3)
ah.add_to_cart(product_id=198412, amount=2)
cart = ah.list_cart()
# Generate invoice
print(json.dumps([
    {
        'product': item['product'].name,
        'quantity': item['quantity'],
        'price': item['product'].price,
        'total': item['quantity'] * item['product'].price
    } for item in cart], indent=2))
# Get total items
print('total items:', sum(item['quantity'] for item in cart))
# Get total items
print('total price:', sum(
    item['quantity']*item['product'].price for item in cart))
```
```json
[
  {
    "product": "AH IJsbergsla voordeel",
    "quantity": 2,
    "price": 1.79,
    "total": 3.58
  },
  {
    "product": "AH Babyspinazie",
    "quantity": 1,
    "price": 1.59,
    "total": 1.59
  },
  {
    "product": "AH Frambozen",
    "quantity": 3,
    "price": 2.39,
    "total": 7.17
  },
  {
    "product": "Valle del sole Popcorn ma\u00efs",
    "quantity": 2,
    "price": 1.53,
    "total": 3.06
  }
]
total items: 8
total price: 15.4
```
