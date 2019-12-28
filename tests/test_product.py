import responses
import pytest
from mijnah.product import PRODUCT_URL, Product


def test_init_err_no_id():
    with pytest.raises(Exception) as excinfo:
        Product()
    assert 'Product id is empty' in str(excinfo.value)


@responses.activate
def test_init_err_no_200():
    responses.add(responses.GET, PRODUCT_URL+'123', status=404)
    with pytest.raises(Exception) as excinfo:
        Product(product_id='123')
    assert 'Error while getting product:' in str(excinfo.value)


@responses.activate
def test_init():
    responses.add(responses.GET, PRODUCT_URL+'42',
                  json={'card': {
                      'products': [{
                          'id': 42,
                          'category': 'foo',
                          'summary': 'bar',
                          'brand': 'fizz',
                          'title': 'buzz',
                          'price': {
                              'now': 123.45
                          }
                      }]
                  }}, status=200)
    product = Product(product_id='42')
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == PRODUCT_URL+'42'
    assert product.id == 42
    assert product.category == 'foo'
    assert product.description == 'bar'
    assert product.brand == 'fizz'
    assert product.price == 123.45
    assert product.name == 'buzz'
    assert repr(product) == 'buzz'
