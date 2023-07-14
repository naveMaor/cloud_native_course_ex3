import httpRequest
from assertions import *

def test_post_three_dishes():
    """
    Test function to insert three dishes using HTTP requests.
    """
    dishes = ["orange", "spaghetti", "apple pie"]
    responses = []

    for dish in dishes:
        response = httpRequest.post("dishes", data={'name': dish})
        responses.append(response)
        assert response.status_code == 201

    assert len(set(response.json() for response in responses)) == len(responses)


def test_get_orange_dish_by_id():
    """
    Test function get the first dish by id expected as orange dish using HTTP requests.
    """
    response = httpRequest.get("/dishes/1")
    assert response.status_code == 200
    sodium_field = response.json()['sodium']
    assert sodium_field >= 0.9 and sodium_field <= 1.1

def test_get_all_three_dishes():
    """
    Test function to get all dishes expected to get three using HTTP requests.
    """
    response = httpRequest.get("dishes")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_post_dish_doesnt_exist():
    """
    Test function to insert a dish that doesn't exist using HTTP requests.
    expected to get -3 as a response.
    """
    dish = "blah"
    response = httpRequest.post("dishes", data={'name': dish})

    assert response.json() == -3
    assert response.status_code == 404 or response.status_code == 400 or response.status_code == 422


def test_post_dish_already_exists():
    """
    Test function to insert a dish that already exists using HTTP requests.
    expected to get -2 as a response.
    """
    dish = "orange"
    response = httpRequest.post("dishes", data={'name': dish})

    assert response.json() == -2
    assert response.status_code == 404 or response.status_code == 400 or response.status_code == 422


def test_post_meal_with_dishes_id():
    """
    Test function to insert a meal with dishes id using HTTP requests.
    expected to get 201 as a response.
    """
    response1 = httpRequest.post("meals", data={'name': "delicious", 'appetizer': 1, 'main': 2, 'dessert': 3})

    assert response1.status_code == 201
    assert response1.json() > 0


def test_get_all_meals():
    """
    Test function to get all meals expected to get one using HTTP requests.
    expected to have one meal in the response and the calories of the meal is between 400 and 500.
    """
    response = httpRequest.get("meals")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()["1"]['cal'] >= 400 and response.json()["1"]['cal'] <= 500


def test_post_meal_already_exists():
    """
    Test function to insert a meal that already exists using HTTP requests.
    expected to get -2 as a response.
    """
    response1 = httpRequest.post("meals", data={'name': "delicious", 'appetizer': 1, 'main': 2, 'dessert': 3})

    assert response1.status_code == 400 or response1.status_code == 422
    assert response1.json() == -2
