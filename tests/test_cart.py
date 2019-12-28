import responses
import pytest
import json
from mijnah.cart import MEMBER_URL, CART_URL, CART_SERVICE_URL, Cart


@pytest.fixture
@responses.activate
def connection():
    responses.add(responses.GET, MEMBER_URL,
                  json={'status': 'ok'}, status=200)
    return Cart(ah_token='my-token')


@responses.activate
def test_init_ah_token():
    responses.add(responses.GET, MEMBER_URL,
                  json={'status': 'ok'}, status=200)
    Cart(ah_token='my-token')
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == MEMBER_URL
    assert responses.calls[0].request.headers['cookie'] == 'ah_token=my-token'


@responses.activate
def test_init_ah_token_presumed():
    responses.add(responses.GET, MEMBER_URL,
                  json={'status': 'ok'}, status=200)
    Cart(ah_token_presumed='my-token')
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == MEMBER_URL
    assert (responses.calls[0].request.headers['cookie']
            == 'ah_token_presumed=my-token')


@responses.activate
def test_init_both_tokens():
    responses.add(responses.GET, MEMBER_URL,
                  json={'status': 'ok'}, status=200)
    Cart(ah_token='my-token', ah_token_presumed='my-presumed-token')
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == MEMBER_URL
    assert (responses.calls[0].request.headers['cookie']
            == 'ah_token=my-token;ah_token_presumed=my-presumed-token')


@responses.activate
def test_init_err_no_token():
    responses.add(responses.GET, MEMBER_URL, status=401)
    with pytest.raises(Exception) as excinfo:
        Cart()
    assert 'Please fill in auth tokens' in str(excinfo.value)

    assert len(responses.calls) == 0


@responses.activate
def test_init_err_bad_response():
    responses.add(responses.GET, MEMBER_URL,
                  json={'foo': 'bar'}, status=401)
    with pytest.raises(Exception) as excinfo:
        Cart(ah_token='foo')
    assert 'Incorrect authentication:' in str(excinfo.value)

    assert len(responses.calls) == 1


@responses.activate
def test_list_cart(connection, mocker):
    mocker.patch('mijnah.cart.Product')
    responses.add(
        responses.GET, CART_URL,
        json={'products': [{
            'id': 123,
            'quantity': 42
        }]}, status=200)
    cart = connection.list_cart()
    assert len(responses.calls) == 1
    assert len(cart) == 1
    assert cart[0]['quantity'] == 42


@responses.activate
def test_empty_cart(connection):
    responses.add(responses.DELETE, CART_SERVICE_URL, status=200)
    connection.empty_cart()
    assert len(responses.calls) == 1


@responses.activate
def test_add_to_cart(connection):
    responses.add(responses.POST, CART_URL+'/add',
                  json={'failed': []}, status=200)
    connection.add_to_cart(123, 42)
    assert len(responses.calls) == 1
    assert json.loads(responses.calls[0].request.body) == {
        'items': [{
            'id': 123,
            'quantity': 42
        }]
    }


@responses.activate
def test_update_cart(connection):
    responses.add(responses.POST, CART_URL+'/update',
                  json={}, status=200)
    connection.update_cart(123, 42)
    assert len(responses.calls) == 1
    assert json.loads(responses.calls[0].request.body) == {
        'items': [{
            'id': 123,
            'quantity': 42
        }]
    }
